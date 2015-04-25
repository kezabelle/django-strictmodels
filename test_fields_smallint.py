# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import SmallIntegerFieldModel
from strictmodels import MODEL_MOMMY_MAPPING


@pytest.mark.django_db
def test_StrictSmallIntegerField_null():
    """
    Cannot be null
    """
    with pytest.raises(ValidationError):
        SmallIntegerFieldModel()


@pytest.mark.django_db
def test_StrictSmallIntegerField_save():
    x = SmallIntegerFieldModel(field='4')
    x.save()
    assert model_to_dict(x) == model_to_dict(SmallIntegerFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictSmallIntegerField_mommy():
    mommy = Mommy(model=SmallIntegerFieldModel)
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


@pytest.mark.django_db
def test_StrictSmallIntegerField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = SmallIntegerFieldModel(field=-500)
    assert value.field == -500
    value.field = 15
    assert value.field == 15
    with pytest.raises(ValidationError):
        value.field = 40000
    assert value.field == 15
    value.field = -4000
    assert value.field == -4000
    with pytest.raises(ValidationError):
        value.field = -40000



@pytest.mark.django_db
def test_StrictSmallIntegerField_string():
    """
    Cannot be null
    """
    with pytest.raises(ValidationError):
        SmallIntegerFieldModel(field='aaaa')


@pytest.mark.django_db
def test_StrictSmallIntegerField_minvalue():
    with pytest.raises(ValidationError):
        SmallIntegerFieldModel(field=-32769)


@pytest.mark.django_db
def test_StrictSmallIntegerField_maxvalue():
    """
    Ensure this value is less than or equal to 15
    """
    with pytest.raises(ValidationError):
        SmallIntegerFieldModel(field=32768)


@pytest.mark.django_db
def test_StrictSmallIntegerField_ok():
    model4 = SmallIntegerFieldModel(field=15)
    assert model4.field == 15


@pytest.mark.django_db
def test_StrictSmallIntegerField_ok_until_changed():
    model5 = SmallIntegerFieldModel(field=15)
    assert model5.field == 15
    with pytest.raises(ValidationError):
        model5.field = 40000


@pytest.mark.django_db
def test_StrictSmallIntegerField_create_via_queryset():
    assert SmallIntegerFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        SmallIntegerFieldModel.objects.create(field=-40000)
    assert SmallIntegerFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictSmallIntegerField_update_via_queryset_invalid_then_get():
    """
    Ensure this value is less than or equal to 15.
    """
    model = SmallIntegerFieldModel.objects.create(field=15)
    model.__class__.objects.filter(pk=model.pk).update(field=40000)
    with pytest.raises(ValidationError):
        model.__class__.objects.get(pk=model.pk)
