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
from fakeapp.models import URLFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_StrictURLField_no_args():
    value = URLFieldModel()


@pytest.mark.django_db
def test_StrictURLField_save():
    x = URLFieldModel(field='http://news.bbc.co.uk/')
    x.save()
    assert model_to_dict(x) == model_to_dict(URLFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictURLField_mommy():
    mommy = Mommy(model=URLFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()


@pytest.mark.django_db
def test_StrictURLField_form_with_instance_valid():
    x = URLFieldModel(field='http://news.bbc.co.uk/')
    form_class = modelform_factory(model=URLFieldModel, fields=['field'])
    form = form_class(data={'field': 'https://cnn.com/'}, instance=x)
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == 'https://cnn.com/'


def test_StrictURLField_form_with_instance_invalid():
    x = URLFieldModel(field='http://news.bbc.co.uk/')
    form_class = modelform_factory(model=URLFieldModel, fields=['field'])
    form = form_class(data={'field': 9223372036854775808}, instance=x)
    assert form.is_valid() is False
    assert form.errors == {'field': ['Enter a valid URL.']}


@pytest.mark.django_db
def test_StrictURLField_form_without_instance_valid():
    form_class = modelform_factory(model=URLFieldModel, fields=['field'])
    form = form_class(data={'field': 'https://cnn.com/'})
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == 'https://cnn.com/'


def test_StrictURLField_form_without_instance_invalid():
    form_class = modelform_factory(model=URLFieldModel, fields=['field'])
    form = form_class(data={'field': 9223372036854775808})
    assert form.is_valid() is False
    assert form.errors == {'field': ['Enter a valid URL.']}


def test_StrictURLField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = URLFieldModel(field='http://t.tt')
    assert value.field == 'http://t.tt'
    value.field = 'https://abc.com'
    assert value.field == 'https://abc.com'
    with pytest.raises(ValidationError):
        value.field = 'v'*256
    assert value.field == 'https://abc.com'
    value.field = 'ftp://bbc.bbc'
    assert value.field == 'ftp://bbc.bbc'
    value.field = None



def test_StrictURLField_values():
    """
    Various conversions, based on the equivalent boolean ones.
    """
    assert URLFieldModel(field='http://t.tt').field == 'http://t.tt'
    assert URLFieldModel(field='https://a.ab').field == 'https://a.ab'
    with pytest.raises(ValidationError):
        assert URLFieldModel(field=1).field == '1'



def test_StrictURLField_values_error_length():
    """
    ValidationError:
    Enter a valid email address
    Ensure this value has at most 200 characters (it has 256)
    """
    newval = 'http://{field}.tt'.format(field='t' * 50)
    assert URLFieldModel(field=newval).field == newval
    with pytest.raises(ValidationError):
        assert URLFieldModel(field='t'*256).field == 't'




def test_StrictURLField_null_skips_cleaning():
    URLFieldModel(field=None)



def test_StrictURLField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state after being set
    """
    model = URLFieldModel(field='http://t.tt')
    with pytest.raises(ValidationError):
        model.field = 't'*256


@pytest.mark.django_db
def test_StrictURLField_create_via_queryset():
    """
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    assert URLFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        URLFieldModel.objects.create(field='t'*256)
    assert URLFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictURLField_update_via_queryset_invalid_then_get():
    """
    So for whatever reason, by the time this gets to the FieldCleaningDescriptor
    the 'blep' has been converted into True ... fun.
    """
    model = URLFieldModel.objects.create(field='http://blepblop.com')
    model.__class__.objects.filter(pk=model.pk).update(field=Decimal('1.011'))
    with pytest.raises(ValidationError):
        model.__class__.objects.get(pk=model.pk).field
