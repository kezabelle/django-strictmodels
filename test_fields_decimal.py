# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict, modelform_factory
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import DecimalFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_StrictDecimalField_no_args():
    value = DecimalFieldModel()


@pytest.mark.django_db
def test_StrictDecimalField_save():
    x = DecimalFieldModel(field='1.1')
    x.save()
    assert model_to_dict(x) == model_to_dict(DecimalFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictDecimalField_mommy():
    mommy = Mommy(model=DecimalFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()


@pytest.mark.django_db
def test_StrictDecimalField_form_with_instance_valid():
    x = DecimalFieldModel(field=5)
    form_class = modelform_factory(model=DecimalFieldModel, fields=['field'])
    form = form_class(data={'field': 6}, instance=x)
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == Decimal('6.0')


def test_StrictDecimalField_form_with_instance_invalid():
    x = DecimalFieldModel(field=5)
    form_class = modelform_factory(model=DecimalFieldModel, fields=['field'])
    form = form_class(data={'field': 9223372036854775808}, instance=x)
    assert form.is_valid() is False
    assert form.errors == {'field': ['Ensure that there are no more than 5 digits in total.']}


@pytest.mark.django_db
def test_StrictDecimalField_form_without_instance_valid():
    form_class = modelform_factory(model=DecimalFieldModel, fields=['field'])
    form = form_class(data={'field': 6})
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == Decimal('6.0')


def test_StrictDecimalField_form_without_instance_invalid():
    form_class = modelform_factory(model=DecimalFieldModel, fields=['field'])
    form = form_class(data={'field': 9223372036854775808})
    assert form.is_valid() is False
    assert form.errors == {'field': ['Ensure that there are no more than 5 digits in total.']}


def test_StrictDecimalField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = DecimalFieldModel(field='1.1')
    assert value.field == Decimal('1.1')
    value.field = '2.0'
    assert value.field == Decimal('2.0')
    with pytest.raises(ValidationError):
        value.field = 'v'*256
    assert value.field == Decimal('2.0')
    value.field = Decimal('3.0')
    assert value.field == Decimal('3.0')
    value.field = -1
    assert value.field == Decimal('-1')
    value.field = '-1'
    assert value.field == Decimal('-1')



def test_StrictDecimalField_null_skips_cleaning():
    DecimalFieldModel(field=None)



def test_StrictDecimalField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state after being set
    """
    model = DecimalFieldModel(field='0.0001')
    assert model.field == Decimal('0.0001')
    with pytest.raises(ValidationError):
        model.field = '2000-00-00'


@pytest.mark.django_db
def test_StrictDecimalField_create_via_queryset():
    """
    This won't allow crap into the DB.
    """
    assert DecimalFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        DecimalFieldModel.objects.create(field='t'*256)
    assert DecimalFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictDecimalField_update_via_queryset_invalid_then_get():
    """
    ValidationError: 2000-01-01' value must be a decimal number
    """
    model = DecimalFieldModel.objects.create(field='0.02')
    assert model.field == Decimal('0.02')
    with pytest.raises(ValidationError):
        model.__class__.objects.filter(pk=model.pk).update(field='2000-01-01')
