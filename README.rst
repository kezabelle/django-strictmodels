django-strictmodels 0.1.0
=========================

An experiment for model fields which automatically do ``clean()`` (thus
validating the data) when setting values, following the principle of
erroring at the earliest opportunity.

The API
-------

I'm hoping this will end up being workable::

    from django.db import models
    from django.db import fields as nonstrict
    import strictmodels as strict

    class MyModel(models.Model):
        a = strict.PositiveIntegerField()
        b = nonstrict.PositiveIntegerField()

And then::

    >>> instance = MyModel(a=1, b=2)
    >>> instance2 = MyModel(a='test', b=2)
    ValidationError: "'test' value must be an integer."

Running the tests
-----------------

Given a complete clone::

    python setup.py test

Or, for a full test::

    tox

Test status
-----------

.. image:: https://travis-ci.org/kezabelle/django-strictmodels.svg?branch=master
  :target: https://travis-ci.org/kezabelle/django-strictmodels

I'd expect nothing but failure, right now.
