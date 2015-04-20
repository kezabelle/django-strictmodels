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

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
        )


class CommaSeparatedIntegerFieldModel(models.Model):
    field = strict.StrictCommaSeparatedIntegerField(max_length=255)

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
        )

class DateFieldModel(models.Model):
    field = strict.StrictDateField()

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )


class DateTimeFieldModel(models.Model):
    field = strict.StrictDateTimeField()

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )


class DecimalFieldModel(models.Model):
    field = strict.StrictDecimalField(max_digits=5, decimal_places=3)

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )


class EmailFieldModel(models.Model):
    field = strict.StrictEmailField()



class FilePathFieldModel(models.Model):
    field = models.FilePathField()



class FloatFieldModel(models.Model):
    field = strict.StrictFloatField()



class GenericIPAddressFieldModel(models.Model):
    field = strict.StrictGenericIPAddressField()



class IntegerFieldModel(models.Model):
    field = strict.StrictIntegerField()



class NullBooleanFieldModel(models.Model):
    field = strict.StrictNullBooleanField()



class PositiveIntegerFieldModel(models.Model):
    field = strict.StrictPositiveIntegerField()



class PositiveSmallIntegerFieldModel(models.Model):
    field = strict.StrictPositiveSmallIntegerField()



class SlugFieldModel(models.Model):
    field = strict.StrictSlugField()



class SmallIntegerFieldModel(models.Model):
    field = strict.StrictSmallIntegerField()



class TextFieldModel(models.Model):
    field = strict.StrictTextField()

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )


class TimeFieldModel(models.Model):
    field = strict.StrictTimeField()



class URLFieldModel(models.Model):
    field = strict.StrictURLField()
