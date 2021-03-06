# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict, modelform_factory
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import NullBooleanFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_StrictNullBooleanField_default():
    """
    Default is null
    """
    value = NullBooleanFieldModel()
    assert value.field is None


@pytest.mark.django_db
def test_StrictNullBooleanField_save():
    x = NullBooleanFieldModel(field=None)
    x.save()
    assert model_to_dict(x) == model_to_dict(NullBooleanFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictNullBooleanField_mommy():
    mommy = Mommy(model=NullBooleanFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()

@pytest.mark.django_db
def test_StrictNullBooleanField_form_with_instance_valid():
    x = NullBooleanFieldModel(field=None)
    form_class = modelform_factory(model=NullBooleanFieldModel, fields=['field'])
    form = form_class(data={'field': '2'}, instance=x)
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field is True


@pytest.mark.django_db
def test_StrictNullBooleanField_form_without_instance_valid():
    form_class = modelform_factory(model=NullBooleanFieldModel, fields=['field'])
    form = form_class(data={'field': 6})
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field is None


def test_StrictNullBooleanField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = NullBooleanFieldModel()
    assert value.field is None
    for x in range(1, 3):
        value.field = False
        assert value.field == False
        with pytest.raises(ValidationError):
            value.field = 'ghost'
        value.field = True
    assert value.field == True



def test_StrictNullBooleanField_trues():
    """
    Cannot be null
    """
    assert NullBooleanFieldModel(field='t').field == True
    assert NullBooleanFieldModel(field='1').field == True
    assert NullBooleanFieldModel(field=1).field == True
    assert NullBooleanFieldModel(field='True').field == True
    assert NullBooleanFieldModel(field=True).field == True



def test_StrictNullBooleanField_false():
    """
    Cannot be null
    """
    assert NullBooleanFieldModel(field='f').field == False
    assert NullBooleanFieldModel(field='0').field == False
    assert NullBooleanFieldModel(field=0).field == False
    assert NullBooleanFieldModel(field='False').field == False
    assert NullBooleanFieldModel(field=False).field == False




def test_StrictNullBooleanField_can_be_null():
    NullBooleanFieldModel(field=None)
    NullBooleanFieldModel(field='None')



def test_StrictNullBooleanField_invalid():
    with pytest.raises(ValidationError):
        NullBooleanFieldModel(field='troo')



def test_StrictNullBooleanField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state
    """
    model = NullBooleanFieldModel(field=True)
    assert model.field == True
    with pytest.raises(ValidationError):
        model.field = 'faaaaalse'


@pytest.mark.django_db
def test_StrictNullBooleanField_create_via_queryset():
    """
    Ensure this value is less than or equal to 15.
    """
    assert NullBooleanFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        NullBooleanFieldModel.objects.create(field=16)
    assert NullBooleanFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictNullBooleanField_update_via_queryset_invalid_then_get():
    """
    So for whatever reason, by the time this gets to the FieldCleaningDescriptor
    the 'blep' has been converted into True ... fun.
    """
    model = NullBooleanFieldModel.objects.create(field=False)
    model.__class__.objects.filter(pk=model.pk).update(field='blep')
    assert model.__class__.objects.get(pk=model.pk).field == True
