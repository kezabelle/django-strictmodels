# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from decimal import Decimal
from django.core.exceptions import ValidationError
import pytest
from fakeapp import models


@pytest.mark.django_db
def test_StrictCsvField_no_args():
    """
    If no args, are given: This field cannot be blank.
    """
    with pytest.raises(ValidationError):
        value = models.CommaSeparatedIntegerFieldModel()




@pytest.mark.django_db
def test_StrictBigIntegerField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = models.CommaSeparatedIntegerFieldModel(field='1,2,3')
    assert value.field == '1,2,3'
    with pytest.raises(ValidationError):
        value.field = 'v'
    assert value.field == '1,2,3'
    value.field = '4,5'
    assert value.field == '4,5'
    with pytest.raises(ValidationError):
        value.field = None


@pytest.mark.django_db
def test_StrictCsvField_values():
    """
    Various conversions, based on the equivalent boolean ones.
    """
    assert models.CommaSeparatedIntegerFieldModel(field='1,2').field == '1,2'
    assert models.CommaSeparatedIntegerFieldModel(field='1').field == '1'
    assert models.CommaSeparatedIntegerFieldModel(field='1,').field == '1,'


@pytest.mark.django_db
def test_StrictCsvField_values_error_length():
    """
    Once an input is too long, error loudly.
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    assert models.CommaSeparatedIntegerFieldModel(field='1,'*10).field == '1,'*10
    with pytest.raises(ValidationError):
        models.CommaSeparatedIntegerFieldModel(field='1,'*200)



@pytest.mark.django_db
def test_StrictCsvField_cant_be_null():
    """
    ValidationError: This field cannot be null
    """
    with pytest.raises(ValidationError):
        models.CommaSeparatedIntegerFieldModel(field=None)


@pytest.mark.django_db
def test_StrictCsvField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state after being set
    """
    model = models.CommaSeparatedIntegerFieldModel(field='1,'*100)
    with pytest.raises(ValidationError):
        model.field = '1,'*256


@pytest.mark.django_db
def test_StrictCsvField_create_via_queryset():
    """
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    assert models.CommaSeparatedIntegerFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        models.CommaSeparatedIntegerFieldModel.objects.create(field='a'*100)
    assert models.CommaSeparatedIntegerFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictCsvField_update_via_queryset_invalid_then_get():
    """
    So for whatever reason, by the time this gets to the FieldCleaningDescriptor
    the 'blep' has been converted into True ... fun.
    """
    model = models.CommaSeparatedIntegerFieldModel.objects.create(field='1,')
    model.__class__.objects.filter(pk=model.pk).update(field=Decimal('1.011'))
    with pytest.raises(ValidationError):
        model.__class__.objects.get(pk=model.pk)
