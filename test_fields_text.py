# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import TextFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_StrictTextField_no_args():
    """
    If no args, are given: This field cannot be blank.
    """
    with pytest.raises(ValidationError):
        value = TextFieldModel()


@pytest.mark.django_db
def test_StrictTextField_save():
    x = TextFieldModel(field='test')
    x.save()
    assert model_to_dict(x) == model_to_dict(TextFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictTextField_mommy():
    mommy = Mommy(model=TextFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()



def test_StrictBigIntegerField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = TextFieldModel(field='t')
    assert value.field == 't'
    value.field = 't'*255
    assert value.field == 't'*255
    assert value.field == 't'*255
    value.field = 'z'*10
    assert value.field == 'z'*10
    value.field = None



def test_StrictTextField_values():
    """
    Various conversions, based on the equivalent boolean ones.
    """
    assert TextFieldModel(field='t').field == 't'
    assert TextFieldModel(field='1').field == '1'
    assert TextFieldModel(field=1).field == '1'
    assert TextFieldModel(field='True').field == 'True'
    assert TextFieldModel(field=True).field == 'True'
    assert TextFieldModel(field='f').field == 'f'
    assert TextFieldModel(field='0').field == '0'
    assert TextFieldModel(field=0).field == '0'
    assert TextFieldModel(field='False').field == 'False'
    assert TextFieldModel(field=False).field == 'False'



def test_StrictTextField_values_length():
    assert TextFieldModel(field='t'*2550).field == 't'*2550




def test_StrictTextField_null_skips_cleaning():
    TextFieldModel(field=None)


@pytest.mark.django_db
def test_StrictTextField_create_via_queryset():
    assert TextFieldModel.objects.count() == 0
    TextFieldModel.objects.create(field='t'*2560)
    assert TextFieldModel.objects.count() == 1


@pytest.mark.django_db
def test_StrictTextField_update_via_queryset_invalid_then_get():
    """
    So for whatever reason, by the time this gets to the FieldCleaningDescriptor
    the 'blep' has been converted into True ... fun.
    """
    model = TextFieldModel.objects.create(field='blep')
    model.__class__.objects.filter(pk=model.pk).update(field=Decimal('1.011'))
    assert model.__class__.objects.get(pk=model.pk).field == '1.011'
