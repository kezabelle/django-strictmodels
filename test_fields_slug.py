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
from fakeapp.models import SlugFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_StrictSlugField_no_args():
    value = SlugFieldModel()


@pytest.mark.django_db
def test_StrictSlugField_save():
    x = SlugFieldModel(field='t-t-t')
    x.save()
    assert model_to_dict(x) == model_to_dict(SlugFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictSlugField_mommy():
    mommy = Mommy(model=SlugFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()


@pytest.mark.django_db
def test_StrictSlugField_form_with_instance_valid():
    x = SlugFieldModel(field='test-a')
    form_class = modelform_factory(model=SlugFieldModel, fields=['field'])
    form = form_class(data={'field': 6}, instance=x)
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == '6'


def test_StrictSlugField_form_with_instance_invalid():
    x = SlugFieldModel(field='test-a')
    form_class = modelform_factory(model=SlugFieldModel, fields=['field'])
    form = form_class(data={'field': '!WWFOIHWBA--$$$#'}, instance=x)
    assert form.is_valid() is False
    assert form.errors == {'field': ["Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens."]}


@pytest.mark.django_db
def test_StrictSlugField_form_without_instance_valid():
    form_class = modelform_factory(model=SlugFieldModel, fields=['field'])
    form = form_class(data={'field': 6})
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == '6'


def test_StrictSlugField_form_without_instance_invalid():
    form_class = modelform_factory(model=SlugFieldModel, fields=['field'])
    form = form_class(data={'field': '!WWFOIHWBA--$$$#'})
    assert form.is_valid() is False
    assert form.errors == {'field': ["Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens."]}


def test_StrictSlugField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = SlugFieldModel(field='t')
    assert value.field == 't'
    value.field = 'a-b-c'
    assert value.field == 'a-b-c'
    with pytest.raises(ValidationError):
        value.field = 'v()'
    assert value.field == 'a-b-c'
    value.field = 'z'*10
    assert value.field == 'z'*10
    value.field = None



def test_StrictSlugField_values():
    """
    Various conversions, based on the equivalent boolean ones.
    """
    assert SlugFieldModel(field='t').field == 't'
    assert SlugFieldModel(field='1').field == '1'
    assert SlugFieldModel(field=1).field == '1'
    assert SlugFieldModel(field='True').field == 'True'
    assert SlugFieldModel(field=True).field == 'True'
    assert SlugFieldModel(field='f').field == 'f'
    assert SlugFieldModel(field='0').field == '0'
    assert SlugFieldModel(field=0).field == '0'
    assert SlugFieldModel(field='False').field == 'False'
    assert SlugFieldModel(field=False).field == 'False'



def test_StrictSlugField_values_error_length():
    """
    Once an input is too long, error loudly.
    ValidationError: Ensure this value has at most 50 characters (it has 51)
    """
    assert SlugFieldModel(field='t').field == 't'
    with pytest.raises(ValidationError):
        assert SlugFieldModel(field='t'*51).field == 't'




def test_StrictSlugField_null_skips_cleaning():
    SlugFieldModel(field=None)



def test_StrictSlugField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state after being set
    """
    model = SlugFieldModel(field='t-b-b-c-d-t-')
    with pytest.raises(ValidationError):
        model.field = 't'*51


@pytest.mark.django_db
def test_StrictSlugField_create_via_queryset():
    """
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    assert SlugFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        SlugFieldModel.objects.create(field='t'*256)
    assert SlugFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictSlugField_update_via_queryset_invalid_then_get():
    """
    Contains invalid slug characters, so can not be retrieved from the DB.
    """
    model = SlugFieldModel.objects.create(field='blep')
    model.__class__.objects.filter(pk=model.pk).update(field=Decimal('1.011'))
    with pytest.raises(ValidationError):
        assert model.__class__.objects.get(pk=model.pk).field == '1.011'
    model.__class__.objects.filter(pk=model.pk).update(field=Decimal('11'))
    assert model.__class__.objects.get(pk=model.pk).field == '11'
