#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division


from django.db.models.fields import __all__ as djangofields

fields = [field for field in djangofields
          if field.endswith('Field') and field != 'Field' and
          field != 'AutoField' and field != 'UUIDField' and
          field != 'DurationField']


MODEL_TEMPLATE = """
class {field}Model(models.Model):
    field = models.{field}()

"""

models = "".join(MODEL_TEMPLATE.format(field=field) for field in fields)


SUBCLASS_TEMPLATE = """
class Strict{field}(fields.{field}):
    def contribute_to_class(self, cls, name, **kwargs):
        super(Strict{field}, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))

"""

subclasses = "".join(SUBCLASS_TEMPLATE.format(field=field) for field in fields)

if __name__ == '__main__':
    print(models)
    print(subclasses)
