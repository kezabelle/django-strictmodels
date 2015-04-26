# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core import validators
from django.db import models
import strictmodels as strict
from django.conf import settings


class BigIntegerFieldModel(models.Model):
    field = strict.StrictBigIntegerField()
    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
        )


class NullBigIntegerFieldModel(models.Model):
    field = strict.StrictBigIntegerField(null=True, blank=True)

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
        )



class BinaryFieldModel(models.Model):
    field = strict.StrictBinaryField()



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

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )

class FilePathFieldModel(models.Model):
    field = strict.StrictFilePathField(path=settings.BASE_DIR)



class FloatFieldModel(models.Model):
    field = strict.StrictFloatField()

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )


class GenericIPAddressFieldModel(models.Model):
    field = strict.StrictGenericIPAddressField()

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )

class IntegerFieldModel(models.Model):
    field = strict.StrictIntegerField()

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )


class NullBooleanFieldModel(models.Model):
    field = strict.StrictNullBooleanField()

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )


class PositiveIntegerFieldModel(models.Model):
    field = strict.StrictPositiveIntegerField()

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )


class PositiveSmallIntegerFieldModel(models.Model):
    field = strict.StrictPositiveSmallIntegerField()

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )

class SlugFieldModel(models.Model):
    field = strict.StrictSlugField()

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )


class SmallIntegerFieldModel(models.Model):
    field = strict.StrictSmallIntegerField()

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )


class TextFieldModel(models.Model):
    field = strict.StrictTextField(max_length=100)

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )


class TimeFieldModel(models.Model):
    field = strict.StrictTimeField()

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )


class URLFieldModel(models.Model):
    field = strict.StrictURLField()

    def __repr__(self):
        return '<{cls!s} pk={pk!r}, field={field!r}>'.format(
            cls=self.__class__.__name__, pk=self.pk, field=self.field,
            )
