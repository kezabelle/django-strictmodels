# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BigIntegerFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(15)])),
            ],
        ),
        migrations.CreateModel(
            name='BinaryFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='BooleanFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CharFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CommaSeparatedIntegerFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.CommaSeparatedIntegerField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DateFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='DateTimeFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='DecimalFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.DecimalField(max_digits=5, decimal_places=3)),
            ],
        ),
        migrations.CreateModel(
            name='EmailFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='FilePathFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.FilePathField(path=b'/Users/kez/Virtualenvs/strictmodels/twat')),
            ],
        ),
        migrations.CreateModel(
            name='FloatFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='GenericIPAddressFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name='IntegerFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NullBigIntegerFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.BigIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(15)])),
            ],
        ),
        migrations.CreateModel(
            name='NullBooleanFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='PositiveIntegerFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PositiveSmallIntegerFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SlugFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='SmallIntegerFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TextFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TimeFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='URLFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.URLField()),
            ],
        ),
    ]
