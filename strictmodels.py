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

    def __repr__(self):
        return "<{mod!s}.{cls!s} field='{field!s}'>".format(
            mod=self.__class__.__module__, cls=self.__class__.__name__,
            field='.'.join((self.field.__class__.__module__,
                            self.field.__class__.__name__)),
        )



class StrictBigIntegerField(fields.BigIntegerField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictBigIntegerField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictBinaryField(fields.BinaryField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictBinaryField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictBooleanField(fields.BooleanField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictBooleanField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictCharField(fields.CharField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictCharField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictCommaSeparatedIntegerField(fields.CommaSeparatedIntegerField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictCommaSeparatedIntegerField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictDateField(fields.DateField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictDateField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictDateTimeField(fields.DateTimeField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictDateTimeField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictDecimalField(fields.DecimalField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictDecimalField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictEmailField(fields.EmailField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictEmailField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictFilePathField(fields.FilePathField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictFilePathField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictFloatField(fields.FloatField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictFloatField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictGenericIPAddressField(fields.GenericIPAddressField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictGenericIPAddressField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictIPAddressField(fields.IPAddressField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictIPAddressField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictIntegerField(fields.IntegerField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictIntegerField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictNullBooleanField(fields.NullBooleanField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictNullBooleanField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictPositiveIntegerField(fields.PositiveIntegerField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictPositiveIntegerField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictPositiveSmallIntegerField(fields.PositiveSmallIntegerField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictPositiveSmallIntegerField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictSlugField(fields.SlugField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictSlugField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictSmallIntegerField(fields.SmallIntegerField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictSmallIntegerField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictTextField(fields.TextField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictTextField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictTimeField(fields.TimeField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictTimeField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictURLField(fields.URLField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictURLField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


try:
    from model_mommy import generators
except ImportError:  # model_mommy is not installed
    MODEL_MOMMY_MAPPING = {}
else:
    MODEL_MOMMY_MAPPING = {
        StrictBooleanField: generators.gen_boolean,
        StrictBigIntegerField: generators.gen_integer,
        StrictCharField: generators.gen_string,
        StrictDateField: generators.gen_date,
        StrictDateTimeField: generators.gen_datetime,
        StrictDecimalField: generators.gen_decimal,
    }
