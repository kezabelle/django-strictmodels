# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
import django
from django.conf import settings
import os


HERE = os.path.realpath(os.path.dirname(__file__))

def pytest_configure():
    if not settings.configured:
        settings.configure(
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:"
                    }
                },
            INSTALLED_APPS=(
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'fakeapp',
            ),
            MIDDLEWARE_CLASSES=(),
            BASE_DIR=HERE,
        )
    if hasattr(django, 'setup'):
        django.setup()
