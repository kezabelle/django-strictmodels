# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
from django.forms import model_to_dict, modelform_factory
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import IntegerFieldModel
from strictmodels import MODEL_MOMMY_MAPPING, SafeModelForm


def test_StrictIntegerField_null():
    IntegerFieldModel()


@pytest.mark.django_db
def test_StrictIntegerField_save():
    x = IntegerFieldModel(field='1')
    x.save()
    assert model_to_dict(x) == model_to_dict(IntegerFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictIntegerField_mommy():
    mommy = Mommy(model=IntegerFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    try:
        mommy.prepare()
    except ValidationError:
        # this is OK because it means our mapping works
        pass
    try:
        mommy.make()
    except ValidationError:
        # this is OK because it means our mapping works
        pass

@pytest.mark.django_db
def test_StrictIntegerField_form_with_instance_valid():
    x = IntegerFieldModel(field=5)
    form_class = modelform_factory(model=IntegerFieldModel, fields=['field'])
    form = form_class(data={'field': 6}, instance=x)
    assert form.is_valid() is True
    assert form.errors == {}
    obj = form.save()
    assert obj == x


def test_StrictIntegerField_form_with_instance_invalid():
    x = IntegerFieldModel(field=5)
    form_class = modelform_factory(model=IntegerFieldModel,
                                   form=SafeModelForm, fields=['field'])
    form = form_class(data={'field': 9223372036854775808}, instance=x)
    assert form.is_valid() is False
    assert form.errors == {'field': ['Ensure this value is less than or equal to 2147483647.']}


@pytest.mark.django_db
def test_StrictIntegerField_form_without_instance_valid():
    form_class = modelform_factory(model=IntegerFieldModel, fields=['field'])
    form = form_class(data={'field': 6})
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == 6


def test_StrictIntegerField_form_without_instance_invalid():
    form_class = modelform_factory(model=IntegerFieldModel,
                                   form=SafeModelForm, fields=['field'])
    form = form_class(data={'field': 9223372036854775808})
    assert form.is_valid() is False
    assert form.errors == {'field': ['Ensure this value is less than or equal to 2147483647.']}

def test_StrictIntegerField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = IntegerFieldModel(field=5)
    assert value.field == 5
    value.field = 15
    assert value.field == 15
    with pytest.raises(ValidationError):
        value.field = 2147483648
    assert value.field == 15
    value.field = 12
    assert value.field == 12



def test_StrictIntegerField_string():
    with pytest.raises(ValidationError):
        IntegerFieldModel(field='aaaa')



def test_StrictIntegerField_minvalue():
    with pytest.raises(ValidationError):
        IntegerFieldModel(field=-2147483649)



def test_StrictIntegerField_maxvalue():
    with pytest.raises(ValidationError):
        IntegerFieldModel(field=2147483648)



def test_StrictIntegerField_ok():
    model4 = IntegerFieldModel(field=15)
    assert model4.field == 15



def test_StrictIntegerField_ok_until_changed():
    model5 = IntegerFieldModel(field=15)
    assert model5.field == 15
    with pytest.raises(ValidationError):
        model5.field = 2147483648


@pytest.mark.django_db
def test_StrictIntegerField_create_via_queryset():
    assert IntegerFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        IntegerFieldModel.objects.create(field=2147483648)
    assert IntegerFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictIntegerField_update_via_queryset_invalid_then_get():
    model = IntegerFieldModel.objects.create(field=15)
    model.__class__.objects.filter(pk=model.pk).update(field=2147483648)
    with pytest.raises(ValidationError):
        model.__class__.objects.get(pk=model.pk)
