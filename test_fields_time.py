# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
from datetime import time
from django.forms import model_to_dict, modelform_factory
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import TimeFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_StrictTimeField_no_args():
    value = TimeFieldModel()


@pytest.mark.django_db
def test_StrictTimeField_save():
    x = TimeFieldModel(field=time())
    x.save()
    assert model_to_dict(x) == model_to_dict(TimeFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictTimeField_mommy():
    mommy = Mommy(model=TimeFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()


@pytest.mark.django_db
def test_StrictTimeField_form_with_instance_valid():
    today = time()
    x = TimeFieldModel(field=today)
    form_class = modelform_factory(model=TimeFieldModel, fields=['field'])
    form = form_class(data={'field': '12:12'}, instance=x)
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == time(12, 12)


def test_StrictTimeField_form_with_instance_invalid():
    today = time()
    x = TimeFieldModel(field=today)
    form_class = modelform_factory(model=TimeFieldModel, fields=['field'])
    form = form_class(data={'field': 9223372036854775808}, instance=x)
    assert form.is_valid() is False
    assert form.errors == {'field': ['Enter a valid time.']}


@pytest.mark.django_db
def test_StrictTimeField_form_without_instance_valid():
    form_class = modelform_factory(model=TimeFieldModel, fields=['field'])
    form = form_class(data={'field': '12:12'})
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == time(12, 12)


def test_StrictTimeField_form_without_instance_invalid():
    form_class = modelform_factory(model=TimeFieldModel, fields=['field'])
    form = form_class(data={'field': 9223372036854775808})
    assert form.is_valid() is False
    assert form.errors == {'field': ['Enter a valid time.']}


def test_StrictTimeField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    today = time()
    value = TimeFieldModel(field=today)
    assert value.field == today
    value.field = '22:22:22'
    assert value.field == time(22, 22, 22)
    with pytest.raises(ValidationError):
        value.field = 'v'*256
    assert value.field == time(22, 22, 22)
    value.field = today
    assert value.field == today
    with pytest.raises(TypeError):
        value.field = -1
    with pytest.raises(ValidationError):
        value.field = '-1'



def test_StrictTimeField_null_skips_cleaning():
    TimeFieldModel(field=None)



def test_StrictTimeField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state after being set
    """
    model = TimeFieldModel(field=time())
    with pytest.raises(ValidationError):
        model.field = '2000-00-00'


@pytest.mark.django_db
def test_StrictTimeField_create_via_queryset():
    """
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    assert TimeFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        TimeFieldModel.objects.create(field='t'*256)
    assert TimeFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictTimeField_update_via_queryset_invalid_then_get():
    """
    So for whatever reason, by the time this gets to the FieldCleaningDescriptor
    the 'blep' has been converted into True ... fun.
    """
    model = TimeFieldModel.objects.create(field=time())
    model.__class__.objects.filter(pk=model.pk).update(field='13:04:01')
    assert model.__class__.objects.get(pk=model.pk).field == time(13, 4, 1)
