# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
import pytest
from fakeapp import models


@pytest.mark.django_db
def test_StrictBooleanField_default():
    """
    Default is null
    """
    value = models.BooleanFieldModel()
    assert value.field == True


@pytest.mark.django_db
def test_StrictBooleanField_trues():
    """
    Cannot be null
    """
    assert models.BooleanFieldModel(field='t').field == True
    assert models.BooleanFieldModel(field='1').field == True
    assert models.BooleanFieldModel(field=1).field == True
    assert models.BooleanFieldModel(field='True').field == True
    assert models.BooleanFieldModel(field=True).field == True


@pytest.mark.django_db
def test_StrictBooleanField_false():
    """
    Cannot be null
    """
    assert models.BooleanFieldModel(field='f').field == False
    assert models.BooleanFieldModel(field='0').field == False
    assert models.BooleanFieldModel(field=0).field == False
    assert models.BooleanFieldModel(field='False').field == False
    assert models.BooleanFieldModel(field=False).field == False



@pytest.mark.django_db
def test_StrictBooleanField_cant_be_null():
    with pytest.raises(ValidationError):
        models.BooleanFieldModel(field=None)


@pytest.mark.django_db
def test_StrictBooleanField_invalid():
    with pytest.raises(ValidationError):
        models.BooleanFieldModel(field='troo')


@pytest.mark.django_db
def test_StrictBooleanField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state
    """
    model = models.BooleanFieldModel(field=True)
    assert model.field == True
    with pytest.raises(ValidationError):
        model.field = 'faaaaalse'


@pytest.mark.django_db
def test_StrictBooleanField_create_via_queryset():
    """
    Ensure this value is less than or equal to 15.
    """
    assert models.BooleanFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        models.BooleanFieldModel.objects.create(field=16)
    assert models.BooleanFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictBooleanField_update_via_queryset_invalid_then_get():
    """
    So for whatever reason, by the time this gets to the FieldCleaningDescriptor
    the 'blep' has been converted into True ... fun.
    """
    model = models.BooleanFieldModel.objects.create(field=False)
    model.__class__.objects.filter(pk=model.pk).update(field='blep')
    assert model.__class__.objects.get(pk=model.pk).field == True
