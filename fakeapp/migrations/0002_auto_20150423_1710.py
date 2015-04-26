# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import strictmodels


class Migration(migrations.Migration):

    dependencies = [
        ('fakeapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='BigIntegerFieldModel',
            name='field',
            field=strictmodels.StrictBigIntegerField(validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(15)]),
        ),
        migrations.AlterField(
            model_name='BinaryFieldModel',
            name='field',
            field=strictmodels.StrictBinaryField(),
        ),
        migrations.AlterField(
            model_name='BooleanFieldModel',
            name='field',
            field=strictmodels.StrictBooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='CharFieldModel',
            name='field',
            field=strictmodels.StrictCharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='CommaSeparatedIntegerFieldModel',
            name='field',
            field=strictmodels.StrictCommaSeparatedIntegerField(max_length=255),
        ),
        migrations.AlterField(
            model_name='DateFieldModel',
            name='field',
            field=strictmodels.StrictDateField(),
        ),
        migrations.AlterField(
            model_name='DateTimeFieldModel',
            name='field',
            field=strictmodels.StrictDateTimeField(),
        ),
        migrations.AlterField(
            model_name='DecimalFieldModel',
            name='field',
            field=strictmodels.StrictDecimalField(max_digits=5, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='EmailFieldModel',
            name='field',
            field=strictmodels.StrictEmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='FilePathFieldModel',
            name='field',
            field=strictmodels.StrictFilePathField(path=b'/Users/kez/Virtualenvs/strictmodels/twat'),
        ),
        migrations.AlterField(
            model_name='FloatFieldModel',
            name='field',
            field=strictmodels.StrictFloatField(),
        ),
        migrations.AlterField(
            model_name='GenericIPAddressFieldModel',
            name='field',
            field=strictmodels.StrictGenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='IntegerFieldModel',
            name='field',
            field=strictmodels.StrictIntegerField(),
        ),
        migrations.AlterField(
            model_name='NullBigIntegerFieldModel',
            name='field',
            field=strictmodels.StrictBigIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(15)]),
        ),
        migrations.AlterField(
            model_name='NullBooleanFieldModel',
            name='field',
            field=strictmodels.StrictNullBooleanField(),
        ),
        migrations.AlterField(
            model_name='PositiveIntegerFieldModel',
            name='field',
            field=strictmodels.StrictPositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='PositiveSmallIntegerFieldModel',
            name='field',
            field=strictmodels.StrictPositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='SlugFieldModel',
            name='field',
            field=strictmodels.StrictSlugField(),
        ),
        migrations.AlterField(
            model_name='SmallIntegerFieldModel',
            name='field',
            field=strictmodels.StrictSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='TextFieldModel',
            name='field',
            field=strictmodels.StrictTextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='TimeFieldModel',
            name='field',
            field=strictmodels.StrictTimeField(),
        ),
        migrations.AlterField(
            model_name='URLFieldModel',
            name='field',
            field=strictmodels.StrictURLField(),
        ),
    ]
