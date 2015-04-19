# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import FloatFieldModel
from strictmodels import MODEL_MOMMY_MAPPING


@pytest.mark.django_db
def test_StrictFloatField_no_args():
    """
    If no args, are given: This field cannot be blank.
    """
    with pytest.raises(ValidationError):
        value = FloatFieldModel()


@pytest.mark.django_db
def test_StrictFloatField_mommy():
    mommy = Mommy(model=FloatFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()


@pytest.mark.django_db
def test_StrictFloatField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = FloatFieldModel(field=1.1)
    assert value.field == 1.1
    value.field = 2.0
    assert value.field == 2.0
    with pytest.raises(ValidationError):
        value.field = 'v'*256
    assert value.field == 2.0
    value.field = 3.0
    assert value.field == 3.0
    value.field = -1
    assert value.field == -1
    value.field = '-1'
    assert value.field == -1


@pytest.mark.django_db
def test_StrictFloatField_cant_be_null():
    """
    ValidationError: This field cannot be null
    """
    with pytest.raises(ValidationError):
        FloatFieldModel(field=None)


@pytest.mark.django_db
def test_StrictFloatField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state after being set
    """
    model = FloatFieldModel(field=0.0001)
    assert model.field == 0.0001
    with pytest.raises(ValidationError):
        model.field = '2000-00-00'


@pytest.mark.django_db
def test_StrictFloatField_create_via_queryset():
    """
    This won't allow crap into the DB.
    """
    assert FloatFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        FloatFieldModel.objects.create(field='t'*256)
    assert FloatFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictFloatField_update_via_queryset_invalid_then_get():
    """
    ValidationError: 2000-01-01' value must be a decimal number
    """
    model = FloatFieldModel.objects.create(field='0.02')
    assert model.field == 0.02
    model.__class__.objects.filter(pk=model.pk).update(field='2000')
    assert model.__class__.objects.get(pk=model.pk).field == 2000.00
