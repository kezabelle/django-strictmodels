# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from fakeapp.models import GFKFieldModel
from model_mommy import mommy
import pytest


@pytest.mark.django_db
def test_StrictGFKField_null():
    GFKFieldModel()


@pytest.mark.django_db
def test_StrictGFKField_save():
    user = mommy.make(get_user_model())
    x = GFKFieldModel(content_object=user)
    x.save()
    assert model_to_dict(x) == model_to_dict(GFKFieldModel.objects.get(pk=x.pk))


@pytest.mark.django_db
def test_StrictGFKField_invalid_data():
    """
    ValidationError: 'object_id': ["'hello I'm not an integer!' value must be an integer."]
    """
    user = mommy.make(get_user_model())
    user.pk = "hello I'm not an integer!"
    with pytest.raises(ValidationError):
        GFKFieldModel(content_object=user)

