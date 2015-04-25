# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import CommaSeparatedIntegerFieldModel
from strictmodels import MODEL_MOMMY_MAPPING


@pytest.mark.django_db
def test_StrictCsvField_no_args():
    """
    If no args, are given: This field cannot be blank.
    """
    with pytest.raises(ValidationError):
        value = CommaSeparatedIntegerFieldModel()


@pytest.mark.django_db
def test_StrictCsvField_save():
    x = CommaSeparatedIntegerFieldModel(field='1,2,3')
    x.save()
    assert model_to_dict(x) == model_to_dict(CommaSeparatedIntegerFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictURLField_mommy():
    mommy = Mommy(model=CommaSeparatedIntegerFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()


@pytest.mark.django_db
def test_StrictBigIntegerField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = CommaSeparatedIntegerFieldModel(field='1,2,3')
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
    assert CommaSeparatedIntegerFieldModel(field='1,2').field == '1,2'
    assert CommaSeparatedIntegerFieldModel(field='1').field == '1'
    assert CommaSeparatedIntegerFieldModel(field='1,').field == '1,'


@pytest.mark.django_db
def test_StrictCsvField_values_error_length():
    """
    Once an input is too long, error loudly.
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    assert CommaSeparatedIntegerFieldModel(field='1,'*10).field == '1,'*10
    with pytest.raises(ValidationError):
        CommaSeparatedIntegerFieldModel(field='1,'*200)



@pytest.mark.django_db
def test_StrictCsvField_cant_be_null():
    """
    ValidationError: This field cannot be null
    """
    with pytest.raises(ValidationError):
        CommaSeparatedIntegerFieldModel(field=None)


@pytest.mark.django_db
def test_StrictCsvField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state after being set
    """
    model = CommaSeparatedIntegerFieldModel(field='1,'*100)
    with pytest.raises(ValidationError):
        model.field = '1,'*256


@pytest.mark.django_db
def test_StrictCsvField_create_via_queryset():
    """
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    assert CommaSeparatedIntegerFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        CommaSeparatedIntegerFieldModel.objects.create(field='a'*100)
    assert CommaSeparatedIntegerFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictCsvField_update_via_queryset_invalid_then_get():
    """
    So for whatever reason, by the time this gets to the FieldCleaningDescriptor
    the 'blep' has been converted into True ... fun.
    """
    model = CommaSeparatedIntegerFieldModel.objects.create(field='1,')
    model.__class__.objects.filter(pk=model.pk).update(field=Decimal('1.011'))
    with pytest.raises(ValidationError):
        model.__class__.objects.get(pk=model.pk)
