from django.db.models import fields

__version_info__ = '0.1.0'
__version__ = '0.1.0'
version = '0.1.0'
def get_version(): return version  # noqa


class FieldCleaningDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))
        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        new_value = self.field.clean(value=value, model_instance=instance)
        instance.__dict__[self.field.name] = new_value
        return new_value



class StrictBigIntegerField(fields.BigIntegerField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictBigIntegerField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))
