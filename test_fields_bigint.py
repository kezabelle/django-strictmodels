# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict, modelform_factory
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import BigIntegerFieldModel, NullBigIntegerFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_StrictBigIntegerField_init():
    """
    No validation is performed, everyone is null
    """
    assert BigIntegerFieldModel().field is None


@pytest.mark.django_db
def test_StrictBigIntegerField_save():
    x = BigIntegerFieldModel(field=5)
    x.save()
    assert model_to_dict(x) == model_to_dict(BigIntegerFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictBigIntegerField_form_with_instance_valid():
    x = BigIntegerFieldModel(field=5)
    form_class = modelform_factory(model=BigIntegerFieldModel, fields=['field'])
    form = form_class(data={'field': 6}, instance=x)
    assert form.is_valid() is True
    assert form.errors == {}
    obj = form.save()
    assert obj == x


def test_StrictBigIntegerField_form_with_instance_invalid():
    x = BigIntegerFieldModel(field=5)
    form_class = modelform_factory(model=BigIntegerFieldModel, fields=['field'])
    form = form_class(data={'field': 9223372036854775808}, instance=x)
    assert form.is_valid() is False
    assert form.errors == {'field': ['Ensure this value is less than or equal to 9223372036854775807.']}


@pytest.mark.django_db
def test_StrictBigIntegerField_form_without_instance_valid():
    form_class = modelform_factory(model=BigIntegerFieldModel, fields=['field'])
    form = form_class(data={'field': 6})
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == 6


def test_StrictBigIntegerField_form_without_instance_invalid():
    form_class = modelform_factory(model=BigIntegerFieldModel, fields=['field'])
    form = form_class(data={'field': 9223372036854775808})
    assert form.is_valid() is False
    assert form.errors == {'field': ['Ensure this value is less than or equal to 9223372036854775807.']}


@pytest.mark.django_db
def test_StrictBigIntegerField_mommy():
    mommy = Mommy(model=BigIntegerFieldModel)
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


def test_StrictBigIntegerField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = BigIntegerFieldModel(field=5)
    assert value.field == 5
    value.field = 15
    assert value.field == 15
    with pytest.raises(ValidationError):
        value.field = 9223372036854775808
    assert value.field == 15
    value.field = 12
    assert value.field == 12



def test_StrictBigIntegerField_nullable():
    """
    Cannot be null
    """
    NullBigIntegerFieldModel(field=None)
    NullBigIntegerFieldModel()
    with pytest.raises(ValidationError):
        NullBigIntegerFieldModel(field=-9223372036854775809)
    with pytest.raises(ValidationError):
        NullBigIntegerFieldModel(field=9223372036854775808)
    NullBigIntegerFieldModel(field=5)



def test_StrictBigIntegerField_string():
    """
    Cannot be null
    """
    with pytest.raises(ValidationError):
        BigIntegerFieldModel(field='aaaa')



def test_StrictBigIntegerField_minvalue():
    with pytest.raises(ValidationError):
        BigIntegerFieldModel(field=-9223372036854775809)



def test_StrictBigIntegerField_maxvalue():
    with pytest.raises(ValidationError):
        BigIntegerFieldModel(field=9223372036854775808)



def test_StrictBigIntegerField_ok():
    model4 = BigIntegerFieldModel(field=15)
    assert model4.field == 15



def test_StrictBigIntegerField_ok_until_changed():
    """
    Ensure this value is less than or equal to 15.
    """
    model5 = BigIntegerFieldModel(field=15)
    assert model5.field == 15
    with pytest.raises(ValidationError):
        model5.field = 9223372036854775808


@pytest.mark.django_db
def test_StrictBigIntegerField_create_via_queryset():
    """
    Ensure this value is less than or equal to 15.
    """
    assert BigIntegerFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        BigIntegerFieldModel.objects.create(field=9223372036854775808)
    assert BigIntegerFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictBigIntegerField_update_via_queryset_invalid_then_get():
    """
    Ensure this value is less than or equal to 15.
    """
    model = BigIntegerFieldModel.objects.create(field=15)
    with pytest.raises(ValidationError):
        model.__class__.objects.filter(pk=model.pk).update(field=9223372036854775808)
    with pytest.raises(ValidationError):
        model.__class__.objects.filter(pk=model.pk).update(field=-9223372036854775809)
