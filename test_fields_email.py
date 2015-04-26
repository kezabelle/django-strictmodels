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
from fakeapp.models import EmailFieldModel
from strictmodels import MODEL_MOMMY_MAPPING



def test_StrictEmailField_no_args():
    value = EmailFieldModel()


@pytest.mark.django_db
def test_StrictEmailField_save():
    x = EmailFieldModel(field='t@t.tt')
    x.save()
    assert model_to_dict(x) == model_to_dict(EmailFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictEmailField_mommy():
    mommy = Mommy(model=EmailFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    mommy.prepare()
    mommy.make()


@pytest.mark.django_db
def test_StrictEmailField_form_with_instance_valid():
    x = EmailFieldModel(field='t@t.tt')
    form_class = modelform_factory(model=EmailFieldModel, fields=['field'])
    form = form_class(data={'field': 'b@b.bb'}, instance=x)
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == 'b@b.bb'


def test_StrictEmailField_form_with_instance_invalid():
    x = EmailFieldModel(field='z@z.zz')
    form_class = modelform_factory(model=EmailFieldModel, fields=['field'])
    form = form_class(data={'field': 9223372036854775808}, instance=x)
    assert form.is_valid() is False
    assert form.errors == {'field': ['Enter a valid email address.']}


@pytest.mark.django_db
def test_StrictEmailField_form_without_instance_valid():
    form_class = modelform_factory(model=EmailFieldModel, fields=['field'])
    form = form_class(data={'field': 'c@cc.cc'})
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.save().field == 'c@cc.cc'


def test_StrictEmailField_form_without_instance_invalid():
    form_class = modelform_factory(model=EmailFieldModel, fields=['field'])
    form = form_class(data={'field': 9223372036854775808})
    assert form.is_valid() is False
    assert form.errors == {'field': ['Enter a valid email address.']}


def test_StrictEmailField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = EmailFieldModel(field='t@t.tt')
    assert value.field == 't@t.tt'
    value.field = 'abc@abc.com'
    assert value.field == 'abc@abc.com'
    with pytest.raises(ValidationError):
        value.field = 'v'*256
    assert value.field == 'abc@abc.com'
    value.field = 'bbc@bbc.bbc'
    assert value.field == 'bbc@bbc.bbc'
    value.field = None



def test_StrictEmailField_values():
    """
    Various conversions, based on the equivalent boolean ones.
    """
    assert EmailFieldModel(field='t@t.tt').field == 't@t.tt'
    assert EmailFieldModel(field='1@1.11').field == '1@1.11'
    with pytest.raises(ValidationError):
        assert EmailFieldModel(field=1).field == '1'



def test_StrictEmailField_values_error_length():
    """
    ValidationError:
    Enter a valid email address
    Ensure this value has at most 254 characters (it has 255)
    """
    newval = 't@{field}.tt'.format(field='t' * 50)
    assert EmailFieldModel(field=newval).field == newval
    with pytest.raises(ValidationError):
        assert EmailFieldModel(field='t'*256).field == 't'




def test_StrictEmailField_null_skips_cleaning():
    EmailFieldModel(field=None)



def test_StrictEmailField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state after being set
    """
    model = EmailFieldModel(field='t@t.tt')
    with pytest.raises(ValidationError):
        model.field = 't'*256


@pytest.mark.django_db
def test_StrictEmailField_create_via_queryset():
    """
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    assert EmailFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        EmailFieldModel.objects.create(field='t'*256)
    assert EmailFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictEmailField_update_via_queryset_invalid_then_get():
    """
    So for whatever reason, by the time this gets to the FieldCleaningDescriptor
    the 'blep' has been converted into True ... fun.
    """
    model = EmailFieldModel.objects.create(field='blep@blop.com')
    model.__class__.objects.filter(pk=model.pk).update(field=Decimal('1.011'))
    # isn't a valid email address when we get it back ...
    with pytest.raises(ValidationError):
        assert model.__class__.objects.get(pk=model.pk).field == '1.011'
