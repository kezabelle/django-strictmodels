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
from fakeapp.models import CharFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_StrictCharField_no_args():
    value = CharFieldModel()


@pytest.mark.django_db
def test_StrictCharField_save():
    x = CharFieldModel(field='test')
    x.save()
    assert model_to_dict(x) == model_to_dict(CharFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictCharField_mommy():
    mommy = Mommy(model=CharFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()


@pytest.mark.django_db
def test_StrictCharField_form_with_instance_valid():
    x = CharFieldModel(field=5)
    form_class = modelform_factory(model=CharFieldModel, fields=['field'])
    # TODO: fix
    form = form_class(data={'field': 6}, instance=x)
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == '6'


def test_StrictCharField_form_with_instance_invalid():
    x = CharFieldModel(field=5)
    form_class = modelform_factory(model=CharFieldModel, fields=['field'])
    form = form_class(data={'field': 't' * 256}, instance=x)
    assert form.is_valid() is False
    assert form.errors == {'field': ['Ensure this value has at most 255 characters (it has 256).']}


@pytest.mark.django_db
def test_StrictCharField_form_without_instance_valid():
    form_class = modelform_factory(model=CharFieldModel, fields=['field'])
    form = form_class(data={'field': 6})
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == '6'


def test_StrictCharField_form_without_instance_invalid():
    form_class = modelform_factory(model=CharFieldModel, fields=['field'])
    form = form_class(data={'field': 't' * 256})
    assert form.is_valid() is False
    assert form.errors == {'field': ['Ensure this value has at most 255 characters (it has 256).']}


def test_StrictCharField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = CharFieldModel(field='t')
    assert value.field == 't'
    value.field = 't'*255
    assert value.field == 't'*255
    with pytest.raises(ValidationError):
        value.field = 'v'*256
    assert value.field == 't'*255
    value.field = 'z'*10
    assert value.field == 'z'*10
    value.field = None
    assert value.field is None



def test_StrictCharField_values():
    """
    Various conversions, based on the equivalent boolean ones.
    """
    assert CharFieldModel(field='t').field == 't'
    assert CharFieldModel(field='1').field == '1'
    assert CharFieldModel(field=1).field == '1'
    assert CharFieldModel(field='True').field == 'True'
    assert CharFieldModel(field=True).field == 'True'
    assert CharFieldModel(field='f').field == 'f'
    assert CharFieldModel(field='0').field == '0'
    assert CharFieldModel(field=0).field == '0'
    assert CharFieldModel(field='False').field == 'False'
    assert CharFieldModel(field=False).field == 'False'



def test_StrictCharField_values_error_length():
    """
    Once an input is too long, error loudly.
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    assert CharFieldModel(field='t'*255).field == 't'*255
    with pytest.raises(ValidationError):
        assert CharFieldModel(field='t'*256).field == 't'




def test_StrictCharField_null_no_cleaning():
    """
    No validation happens on Nones because of Django doing setattr(None)
    """
    CharFieldModel(field=None)



def test_StrictCharField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state after being set
    """
    model = CharFieldModel(field='t'*100)
    with pytest.raises(ValidationError):
        model.field = 't'*256


@pytest.mark.django_db
def test_StrictCharField_create_via_queryset():
    """
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    assert CharFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        CharFieldModel.objects.create(field='t'*256)
    assert CharFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictCharField_update_via_queryset_invalid_then_get():
    """
    So for whatever reason, by the time this gets to the FieldCleaningDescriptor
    the 'blep' has been converted into True ... fun.
    """
    model = CharFieldModel.objects.create(field='blep')
    model.__class__.objects.filter(pk=model.pk).update(field=Decimal('1.011'))
    assert model.__class__.objects.get(pk=model.pk).field == '1.011'
