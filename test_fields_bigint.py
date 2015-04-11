# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
import pytest
from fakeapp import models


@pytest.mark.django_db
def test_StrictBigIntegerField_null():
    """
    Cannot be null
    """
    with pytest.raises(ValidationError):
        models.BigIntegerFieldModel()


@pytest.mark.django_db
def test_StrictBigIntegerField_string():
    """
    Cannot be null
    """
    with pytest.raises(ValidationError):
        models.BigIntegerFieldModel(field='aaaa')


@pytest.mark.django_db
def test_StrictBigIntegerField_minvalue():
    """
    Ensure this value is greater than or equal to 5
    """
    with pytest.raises(ValidationError):
        models.BigIntegerFieldModel(field=1)


@pytest.mark.django_db
def test_StrictBigIntegerField_maxvalue():
    """
    Ensure this value is less than or equal to 15
    """
    with pytest.raises(ValidationError):
        models.BigIntegerFieldModel(field=16)


@pytest.mark.django_db
def test_StrictBigIntegerField_ok():
    model4 = models.BigIntegerFieldModel(field=15)
    assert model4.field == 15


@pytest.mark.django_db
def test_StrictBigIntegerField_ok_until_changed():
    """
    Ensure this value is less than or equal to 15.
    """
    model5 = models.BigIntegerFieldModel(field=15)
    assert model5.field == 15
    with pytest.raises(ValidationError):
        model5.field = 16


@pytest.mark.django_db
def test_StrictBigIntegerField_create_via_queryset():
    """
    Ensure this value is less than or equal to 15.
    """
    assert models.BigIntegerFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        models.BigIntegerFieldModel.objects.create(field=16)
    assert models.BigIntegerFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictBigIntegerField_update_via_queryset_invalid_then_get():
    """
    Ensure this value is less than or equal to 15.
    """
    model = models.BigIntegerFieldModel.objects.create(field=15)
    model.__class__.objects.filter(pk=model.pk).update(field=16)
    with pytest.raises(ValidationError):
        model.__class__.objects.get(pk=model.pk)
