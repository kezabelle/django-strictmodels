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

Note that this model is a combination of strict and normal model fields,
which would allow for gradual hardening::

    >>> instance = MyModel(a=1, b=2)
    >>> instance2 = MyModel(a='test', b=2)
    ValidationError: "'test' value must be an integer."

Because ``a`` is cleaned on assignment, we receive a handy error, just like
with forms. Meanwhile, doing the following would not raise an error,
because ``b`` is a normal Django field::

    >>> instance3 = MyModel(a=1, b='test')

At least not at *that* point.

Implemented fields
------------------

Currently, the available fields which have at least some testing, are:

* ``strictmodels.StrictBigIntegerField`` (subclasses ``BigIntegerField``)

  * will only allow -9223372036854775808 to 9223372036854775807
  
* ``strictmodels.StrictBooleanField`` (subclasses ``BooleanField``)
* ``strictmodels.StrictNullBooleanField`` (subclasses ``NullBooleanField``)
* ``strictmodels.StrictCharField`` (subclasses ``CharField``)
* ``strictmodels.StrictTextField`` (subclasses ``TextField``)
* ``strictmodels.StrictCommaSeparatedIntegerField`` (subclasses ``CommaSeparatedIntegerField``)
* ``strictmodels.StrictDateField`` (subclasses ``DateField``)
* ``strictmodels.StrictDateTimeField`` (subclasses ``DateTimeField``)
* ``strictmodels.StrictTimeField`` (subclasses ``TimeField``)
* ``strictmodels.StrictDecimalField`` (subclasses ``DecimalField``)
* ``strictmodels.StrictEmailField`` (subclasses ``EmailField``)

  * Will only allow string sequences that pass an emailish regular expression.

* ``strictmodels.StrictFilePathField`` (subclasses ``FilePathField``)

  * Will only allow strings whose path is within that set on the field itself.

* ``strictmodels.StrictFloatField`` (subclasses ``FloatField``)
* ``strictmodels.StrictGenericIPAddressField`` (subclasses ``GenericIPAddressField``)
* ``strictmodels.StrictIntegerField`` (subclasses ``IntegerField``)

  * will only allow -2147483648 to 2147483647

* ``strictmodels.StrictPositiveIntegerField`` (subclasses ``PositiveIntegerField``)

  * will only allow 0 to 2147483647

* ``strictmodels.StrictSmallIntegerField`` (subclasses ``SmallIntegerField``)

  * will only allow -32768 to 32767

* ``strictmodels.StrictPositiveSmallIntegerField`` (subclasses ``PositiveSmallIntegerField``)

  * will only allow 0 to 32767

* ``strictmodels.StrictSlugField`` (subclasses ``SlugField``)
* ``strictmodels.StrictURLField`` (subclasses ``URLField``)

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
