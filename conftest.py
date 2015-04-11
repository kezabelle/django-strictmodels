# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
import django
from django.conf import settings

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
                'fakeapp',
            ),
            MIDDLEWARE_CLASSES=(),
        )
    if hasattr(django, 'setup'):
        django.setup()
