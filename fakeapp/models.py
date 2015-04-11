# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core import validators
from django.db import models
import strictmodels as strict


class BigIntegerFieldModel(models.Model):
    field = strict.StrictBigIntegerField(validators=[
        validators.MinValueValidator(5),
        validators.MaxValueValidator(15)
    ])
