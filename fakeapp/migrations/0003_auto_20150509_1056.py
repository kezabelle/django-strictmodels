# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import strictmodels


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('fakeapp', '0002_auto_20150423_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='GFKFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', strictmodels.StrictPositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.AlterField(
            model_name='BigIntegerFieldModel',
            name='field',
            field=strictmodels.StrictBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='FilePathFieldModel',
            name='field',
            field=strictmodels.StrictFilePathField(path=b'/Users/kez/Virtualenvs/strictmodels/ffs'),
        ),
        migrations.AlterField(
            model_name='NullBigIntegerFieldModel',
            name='field',
            field=strictmodels.StrictBigIntegerField(null=True, blank=True),
        ),
    ]
