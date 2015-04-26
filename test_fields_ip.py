# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
from django.forms import model_to_dict, modelform_factory
from model_mommy.mommy import Mommy
import pytest
from fakeapp.models import GenericIPAddressFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_StrictGenericIPAddressField_no_args():
    value = GenericIPAddressFieldModel()


@pytest.mark.django_db
def test_StrictGenericIPAddressField_save():
    x = GenericIPAddressFieldModel(field='127.0.0.1')
    x.save()
    assert model_to_dict(x) == model_to_dict(GenericIPAddressFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictGenericIPAddressField_mommy():
    mommy = Mommy(model=GenericIPAddressFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()


@pytest.mark.django_db
def test_StrictGenericIPAddressField_form_with_instance_valid():
    x = GenericIPAddressFieldModel(field='127.0.0.1')
    form_class = modelform_factory(model=GenericIPAddressFieldModel, fields=['field'])
    form = form_class(data={'field': '255.255.255.255'}, instance=x)
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == '255.255.255.255'


def test_StrictGenericIPAddressField_form_with_instance_invalid():
    x = GenericIPAddressFieldModel(field='127.0.0.1')
    form_class = modelform_factory(model=GenericIPAddressFieldModel, fields=['field'])
    form = form_class(data={'field': 'ghost'}, instance=x)
    assert form.is_valid() is False
    assert form.errors == {'field': ['Enter a valid IPv4 or IPv6 address.']}


@pytest.mark.django_db
def test_StrictGenericIPAddressField_form_without_instance_valid():
    form_class = modelform_factory(model=GenericIPAddressFieldModel, fields=['field'])
    form = form_class(data={'field': '255.255.255.255'})
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == '255.255.255.255'


def test_StrictGenericIPAddressField_form_without_instance_invalid():
    form_class = modelform_factory(model=GenericIPAddressFieldModel, fields=['field'])
    form = form_class(data={'field': 'shark'})
    assert form.is_valid() is False
    assert form.errors == {'field': ['Enter a valid IPv4 or IPv6 address.']}


def test_StrictGenericIPAddressField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = GenericIPAddressFieldModel(field='127.0.0.1')
    assert value.field == '127.0.0.1'
    value.field = '127.0.0.2'
    assert value.field == '127.0.0.2'
    with pytest.raises(ValidationError):
        value.field = 'v'*256
    assert value.field == '127.0.0.2'
    value.field = '192.168.0.1'
    assert value.field == '192.168.0.1'
    value.field = None



def test_StrictGenericIPAddressField_values_error_length():
    """
    Once an input is too long, error loudly.
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    ok = '2001:0db8:85a3:0042:1000:8a2e:0370:7334'
    notok = '2001:0db8:85a3:0042:1000:8a2e:0370:7334a'
    assert GenericIPAddressFieldModel(field=ok).field == '2001:db8:85a3:42:1000:8a2e:370:7334' # noqa
    with pytest.raises(ValidationError):
        GenericIPAddressFieldModel(field=notok)




def test_StrictGenericIPAddressField_null_skips_cleaning():
    GenericIPAddressFieldModel(field=None)



def test_StrictGenericIPAddressField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state after being set
    """
    model = GenericIPAddressFieldModel(field='2001:0::0:01')
    with pytest.raises(ValidationError):
        model.field = 't'*256


@pytest.mark.django_db
def test_StrictGenericIPAddressField_create_via_queryset():
    """
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    assert GenericIPAddressFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        GenericIPAddressFieldModel.objects.create(field='t'*256)
    assert GenericIPAddressFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictGenericIPAddressField_update_via_queryset_invalid_then_get():
    model = GenericIPAddressFieldModel.objects.create(field='127.0.0.1')
    model.__class__.objects.filter(pk=model.pk).update(field='2.2.2.2.2.2.2.2')
    with pytest.raises(ValidationError):
        model.__class__.objects.get(pk=model.pk)
