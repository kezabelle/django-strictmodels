# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from model_mommy.mommy import Mommy
import os
import pytest
from fakeapp.models import FilePathFieldModel
from strictmodels import MODEL_MOMMY_MAPPING

HERE = os.path.realpath(os.path.dirname(__file__))
GOOD_FILE = os.path.join(HERE, 'test_fields_filepath.py')
GOOD_FILE2 = os.path.join(HERE, 'test_fields_ip.py')
BAD_FILE = os.path.join(HERE, 'this_file_should_never_exist_hopefully.exe')



def test_StrictFilePathField_no_args():
    """
    If no args, are given: This field cannot be blank.
    """
    with pytest.raises(ValidationError):
        value = FilePathFieldModel()


@pytest.mark.django_db
def test_StrictFilePathField_save():
    x = FilePathFieldModel(field=GOOD_FILE)
    x.save()
    assert model_to_dict(x) == model_to_dict(FilePathFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictFilePathField_mommy():
    mommy = Mommy(model=FilePathFieldModel)
    mommy.type_mapping.update(MODEL_MOMMY_MAPPING)
    with pytest.raises(TypeError):
        mommy.prepare()
    with pytest.raises(TypeError):
        mommy.make()



def test_StrictFilePathField_descriptor_doesnt_disappear():
    """
    don't clobber the descriptor
    """
    value = FilePathFieldModel(field=GOOD_FILE)
    assert value.field == GOOD_FILE
    with pytest.raises(ValidationError):
        value.field = BAD_FILE
    assert value.field == GOOD_FILE
    value.field = GOOD_FILE2
    assert value.field == GOOD_FILE2
    with pytest.raises(ValidationError):
        value.field = None



def test_StrictFilePathField_cant_be_null():
    """
    ValidationError: This field cannot be null
    """
    with pytest.raises(ValidationError):
        FilePathFieldModel(field=None)



def test_StrictFilePathField_ok_until_changed():
    """
    Ensure this value cannot change to an invalid state after being set
    """
    model = FilePathFieldModel(field=GOOD_FILE)
    with pytest.raises(ValidationError):
        model.field = BAD_FILE


@pytest.mark.django_db
def test_StrictFilePathField_create_via_queryset():
    """
    ValidationError: Ensure this value has at most 255 characters (it has 256)
    """
    assert FilePathFieldModel.objects.count() == 0
    with pytest.raises(ValidationError):
        FilePathFieldModel.objects.create(field='t'*256)
    assert FilePathFieldModel.objects.count() == 0


@pytest.mark.django_db
def test_StrictFilePathField_update_via_queryset_invalid_then_get():
    model = FilePathFieldModel.objects.create(field=GOOD_FILE)
    model.__class__.objects.filter(pk=model.pk).update(field=BAD_FILE)
    with pytest.raises(ValidationError):
        model.__class__.objects.get(pk=model.pk)
