# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.utils.datetime_safe import datetime
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import DateTimeFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_StrictDateTimeField_no_args():
    value = DateTimeFieldModel()


@pytest.mark.django_db
def test_StrictDateTimeField_save():
    x = DateTimeFieldModel(field=datetime.today())
    x.save()
    assert model_to_dict(x) == model_to_dict(DateTimeFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictDateTimeField_mommy():
    mommy = Mommy(model=DateTimeFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()



def test_StrictDateTimeField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    today = datetime.today()
    value = DateTimeFieldModel(field=today)
    assert value.field == today
    value.field = '2015-04-16'
    assert value.field == datetime(2015, 4, 16, 0, 0)
    with pytest.raises(ValidationError):
        value.field = 'v'*256
    assert value.field == datetime(2015, 4, 16, 0, 0)
    value.field = today
    assert value.field == today
    with pytest.raises(TypeError):
        value.field = -1
    with pytest.raises(ValidationError):
        value.field = '-1'



def test_StrictDateTimeField_null_skips_cleaning():
    DateTimeFieldModel(field=None)



def test_StrictDateTimeField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state after being set
    """
    model = DateTimeFieldModel(field=datetime.today())
    with pytest.raises(ValidationError):
        model.field = '2000-00-00'


@pytest.mark.django_db
def test_StrictDateTimeField_create_via_queryset():
    """
    This won't allow crap into the DB.
    """
    assert DateTimeFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        DateTimeFieldModel.objects.create(field='t'*256)
    assert DateTimeFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictDateTimeField_update_via_queryset_invalid_then_get():
    """
    So for whatever reason, by the time this gets to the FieldCleaningDescriptor
    the 'blep' has been converted into True ... fun.
    """
    model = DateTimeFieldModel.objects.create(field=datetime.today())
    model.__class__.objects.filter(pk=model.pk).update(field='2000-01-01')
    assert model.__class__.objects.get(pk=model.pk).field == datetime(2000, 1, 1, 0, 0)
