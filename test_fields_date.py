# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.utils.datetime_safe import date
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import DateFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_StrictDateField_no_args():
    """
    If no args, are given: This field cannot be blank.
    """
    with pytest.raises(ValidationError):
        value = DateFieldModel()


@pytest.mark.django_db
def test_StrictDateField_save():
    x = DateFieldModel(field=date.today())
    x.save()
    assert model_to_dict(x) == model_to_dict(DateFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictDateField_mommy():
    mommy = Mommy(model=DateFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()



def test_StrictDateField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    today = date.today()
    value = DateFieldModel(field=today)
    assert value.field == today
    value.field = '2015-04-16'
    assert value.field == date(2015, 4, 16)
    with pytest.raises(ValidationError):
        value.field = 'v'*256
    assert value.field == date(2015, 4, 16)
    value.field = today
    assert value.field == today
    with pytest.raises(TypeError):
        value.field = -1
    with pytest.raises(ValidationError):
        value.field = '-1'



def test_StrictDateField_cant_be_null():
    """
    ValidationError: This field cannot be null
    """
    with pytest.raises(ValidationError):
        DateFieldModel(field=None)



def test_StrictDateField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state after being set
    """
    model = DateFieldModel(field=date.today())
    with pytest.raises(ValidationError):
        model.field = '2000-00-00'


@pytest.mark.django_db
def test_StrictDateField_create_via_queryset():
    """
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    assert DateFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        DateFieldModel.objects.create(field='t'*256)
    assert DateFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictDateField_update_via_queryset_invalid_then_get():
    """
    So for whatever reason, by the time this gets to the FieldCleaningDescriptor
    the 'blep' has been converted into True ... fun.
    """
    model = DateFieldModel.objects.create(field=date.today())
    model.__class__.objects.filter(pk=model.pk).update(field='2000-01-01')
    assert model.__class__.objects.get(pk=model.pk).field == date(2000, 1, 1)
