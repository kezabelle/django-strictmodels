# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import BooleanFieldModel
from strictmodels import MODEL_MOMMY_MAPPING


@pytest.mark.django_db
def test_StrictBooleanField_default():
    """
    Default is null
    """
    value = BooleanFieldModel()
    assert value.field == True


@pytest.mark.django_db
def test_StrictBooleanField_mommy():
    mommy = Mommy(model=BooleanFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()


@pytest.mark.django_db
def test_StrictBooleanField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = BooleanFieldModel()
    assert value.field == True
    for x in range(1, 3):
        value.field = False
        assert value.field == False
        with pytest.raises(ValidationError):
            value.field = 'ghost'
        value.field = True
    assert value.field == True


@pytest.mark.django_db
def test_StrictBooleanField_trues():
    """
    Cannot be null
    """
    assert BooleanFieldModel(field='t').field == True
    assert BooleanFieldModel(field='1').field == True
    assert BooleanFieldModel(field=1).field == True
    assert BooleanFieldModel(field='True').field == True
    assert BooleanFieldModel(field=True).field == True


@pytest.mark.django_db
def test_StrictBooleanField_false():
    """
    Cannot be null
    """
    assert BooleanFieldModel(field='f').field == False
    assert BooleanFieldModel(field='0').field == False
    assert BooleanFieldModel(field=0).field == False
    assert BooleanFieldModel(field='False').field == False
    assert BooleanFieldModel(field=False).field == False



@pytest.mark.django_db
def test_StrictBooleanField_cant_be_null():
    with pytest.raises(ValidationError):
        BooleanFieldModel(field=None)


@pytest.mark.django_db
def test_StrictBooleanField_invalid():
    with pytest.raises(ValidationError):
        BooleanFieldModel(field='troo')


@pytest.mark.django_db
def test_StrictBooleanField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state
    """
    model = BooleanFieldModel(field=True)
    assert model.field == True
    with pytest.raises(ValidationError):
        model.field = 'faaaaalse'


@pytest.mark.django_db
def test_StrictBooleanField_create_via_queryset():
    """
    Ensure this value is less than or equal to 15.
    """
    assert BooleanFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        BooleanFieldModel.objects.create(field=16)
    assert BooleanFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictBooleanField_update_via_queryset_invalid_then_get():
    """
    So for whatever reason, by the time this gets to the FieldCleaningDescriptor
    the 'blep' has been converted into True ... fun.
    """
    model = BooleanFieldModel.objects.create(field=False)
    model.__class__.objects.filter(pk=model.pk).update(field='blep')
    assert model.__class__.objects.get(pk=model.pk).field == True
