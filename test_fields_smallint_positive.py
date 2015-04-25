# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import PositiveSmallIntegerFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_PositiveSmallIntegerField_null():
    """
    Cannot be null
    """
    with pytest.raises(ValidationError):
        PositiveSmallIntegerFieldModel()


@pytest.mark.django_db
def test_PositiveSmallIntegerField_save():
    x = PositiveSmallIntegerFieldModel(field='4')
    x.save()
    assert model_to_dict(x) == model_to_dict(PositiveSmallIntegerFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_PositiveSmallIntegerField_mommy():
    mommy = Mommy(model=PositiveSmallIntegerFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    try:
        mommy.prepare()
    except ValidationError:
        # this is OK because it means our mapping works
        pass
    try:
        mommy.make()
    except ValidationError:
        # this is OK because it means our mapping works
        pass



def test_PositiveSmallIntegerField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = PositiveSmallIntegerFieldModel(field=1)
    assert value.field == 1
    value.field = 15
    assert value.field == 15
    with pytest.raises(ValidationError):
        value.field = 40000
    assert value.field == 15
    value.field = 2
    assert value.field == 2
    with pytest.raises(ValidationError):
        value.field = -1




def test_PositiveSmallIntegerField_string():
    """
    Cannot be null
    """
    with pytest.raises(ValidationError):
        PositiveSmallIntegerFieldModel(field='aaaa')



def test_PositiveSmallIntegerField_minvalue():
    PositiveSmallIntegerFieldModel(field=0)
    with pytest.raises(ValidationError):
        PositiveSmallIntegerFieldModel(field=-1)



def test_PositiveSmallIntegerField_maxvalue():
    PositiveSmallIntegerFieldModel(field=32767)
    with pytest.raises(ValidationError):
        PositiveSmallIntegerFieldModel(field=32768)



def test_PositiveSmallIntegerField_ok():
    model4 = PositiveSmallIntegerFieldModel(field=15)
    assert model4.field == 15



def test_PositiveSmallIntegerField_ok_until_changed():
    model5 = PositiveSmallIntegerFieldModel(field=15)
    assert model5.field == 15
    with pytest.raises(ValidationError):
        model5.field = 40000


@pytest.mark.django_db
def test_PositiveSmallIntegerField_create_via_queryset():
    assert PositiveSmallIntegerFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        PositiveSmallIntegerFieldModel.objects.create(field=-40000)
    assert PositiveSmallIntegerFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_PositiveSmallIntegerField_update_via_queryset_invalid_then_get():
    """
    Ensure this value is less than or equal to 15.
    """
    model = PositiveSmallIntegerFieldModel.objects.create(field=15)
    model.__class__.objects.filter(pk=model.pk).update(field=40000)
    with pytest.raises(ValidationError):
        model.__class__.objects.get(pk=model.pk)
