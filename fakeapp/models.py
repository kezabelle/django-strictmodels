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

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
        )


class NullBigIntegerFieldModel(models.Model):
    field = strict.StrictBigIntegerField(validators=[
        validators.MinValueValidator(5),
        validators.MaxValueValidator(15)
    ], null=True, blank=True)

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
        )



class BinaryFieldModel(models.Model):
    field = models.BinaryField()



class BooleanFieldModel(models.Model):
    field = strict.StrictBooleanField(default=True)

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
        )



class CharFieldModel(models.Model):
    field = strict.StrictCharField(max_length=255, blank=False)



class CommaSeparatedIntegerFieldModel(models.Model):
    field = models.CommaSeparatedIntegerField(max_length=255)



class DateFieldModel(models.Model):
    field = models.DateField()



class DateTimeFieldModel(models.Model):
    field = models.DateTimeField()



class DecimalFieldModel(models.Model):
    field = models.DecimalField(max_digits=5, decimal_places=3)



class EmailFieldModel(models.Model):
    field = models.EmailField()



class FilePathFieldModel(models.Model):
    field = models.FilePathField()



class FloatFieldModel(models.Model):
    field = models.FloatField()



class GenericIPAddressFieldModel(models.Model):
    field = models.GenericIPAddressField()



class IPAddressFieldModel(models.Model):
    field = models.IPAddressField()



class IntegerFieldModel(models.Model):
    field = models.IntegerField()



class NullBooleanFieldModel(models.Model):
    field = models.NullBooleanField()



class PositiveIntegerFieldModel(models.Model):
    field = models.PositiveIntegerField()



class PositiveSmallIntegerFieldModel(models.Model):
    field = models.PositiveSmallIntegerField()



class SlugFieldModel(models.Model):
    field = models.SlugField()



class SmallIntegerFieldModel(models.Model):
    field = models.SmallIntegerField()



class TextFieldModel(models.Model):
    field = models.TextField()



class TimeFieldModel(models.Model):
    field = models.TimeField()



class URLFieldModel(models.Model):
    field = models.URLField()
