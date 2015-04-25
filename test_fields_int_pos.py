# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import PositiveIntegerFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_StrictPositiveIntegerField_null():
    """
    Cannot be null
    """
    with pytest.raises(ValidationError):
        PositiveIntegerFieldModel()


@pytest.mark.django_db
def test_StrictPositiveIntegerField_save():
    x = PositiveIntegerFieldModel(field='1')
    x.save()
    assert model_to_dict(x) == model_to_dict(PositiveIntegerFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictPositiveIntegerField_mommy():
    mommy = Mommy(model=PositiveIntegerFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()



def test_StrictPositiveIntegerField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = PositiveIntegerFieldModel(field=5)
    assert value.field == 5
    value.field = 15
    assert value.field == 15
    with pytest.raises(ValidationError):
        value.field = 2147483648
    assert value.field == 15
    value.field = 12
    assert value.field == 12



def test_StrictPositiveIntegerField_string():
    with pytest.raises(ValidationError):
        PositiveIntegerFieldModel(field='aaaa')



def test_StrictPositiveIntegerField_minvalue():
    with pytest.raises(ValidationError):
        PositiveIntegerFieldModel(field=-1)



def test_StrictPositiveIntegerField_maxvalue():
    with pytest.raises(ValidationError):
        PositiveIntegerFieldModel(field=2147483648)



def test_StrictPositiveIntegerField_ok():
    model4 = PositiveIntegerFieldModel(field=15)
    assert model4.field == 15



def test_StrictPositiveIntegerField_ok_until_changed():
    model5 = PositiveIntegerFieldModel(field=15)
    assert model5.field == 15
    with pytest.raises(ValidationError):
        model5.field = 2147483648


@pytest.mark.django_db
def test_StrictPositiveIntegerField_create_via_queryset():
    assert PositiveIntegerFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        PositiveIntegerFieldModel.objects.create(field=2147483648)
    assert PositiveIntegerFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictPositiveIntegerField_update_via_queryset_invalid_then_get():
    model = PositiveIntegerFieldModel.objects.create(field=15)
    model.__class__.objects.filter(pk=model.pk).update(field=2147483648)
    with pytest.raises(ValidationError):
        model.__class__.objects.get(pk=model.pk)
