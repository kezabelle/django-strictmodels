from django.core.exceptions import FieldError, ValidationError
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator,
                                    MaxLengthValidator)
from django.db.models import fields
from django.forms import ModelForm
from django.utils import six
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

__version_info__ = '0.1.0'
__version__ = '0.1.0'
version = '0.1.0'
def get_version(): return version  # noqa


class SafeModelForm(ModelForm):
    """
    This is necessary to avoid exceptions bubbling and not being caught
    by the is_valid call.
    See https://code.djangoproject.com/ticket/24706#ticket
    """
    def _post_clean(self):
        try:
            super(SafeModelForm, self)._post_clean()
        except ValidationError as e:
            # This is necessary to avoid getting
            # AttributeError: 'ValidationError' object has no attribute 'error_dict'
            # when trying to _update_errors
            errors = {}
            errors = e.update_error_dict(errors)
            self._update_errors(ValidationError(errors))


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
        """
        We special-case None to not do any validation (regardless of nullability)
        because of the various ways which Django likes to instantiate objects
        with null values. Mostly in ModelBase.__init__,
        forms.models.construct_instance etc
        """
        if value is None:
            new_value = value
        else:
            # check whether it's the default value for the field, which we also
            # don't clean because of charfields etc.
            field_default = self.field.get_default()
            if value == field_default:
                new_value = field_default
            else:
                # if not None/the field's default, validate it ...
                try:
                    new_value = self.field.clean(value=value, model_instance=instance)
                except ValidationError as exc:
                    # catch and re-raise it as a dict mapping key: exception
                    # so that forms will attribute it to the correct field.
                    raise ValidationError(message={
                        self.field.name: exc.messages,
                    }, code=getattr(exc, 'code', None))
        instance.__dict__[self.field.name] = new_value
        return new_value

    def __repr__(self):
        return "<{mod!s}.{cls!s} field='{field!s}'>".format(
            mod=self.__class__.__module__, cls=self.__class__.__name__,
            field='.'.join((self.field.__class__.__module__,
                            self.field.__class__.__name__)),
        )



class StrictBigIntegerField(fields.BigIntegerField):
    default_validators = [
        MinValueValidator(-9223372036854775808),
        MaxValueValidator(9223372036854775807)
    ]
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictBigIntegerField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))

    def get_db_prep_value(self, *args, **kwargs):
        value = super(StrictBigIntegerField, self).get_db_prep_value(*args, **kwargs)
        self.run_validators(value)
        return value


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
    def to_python(self, value):
        if isinstance(value, six.string_types) or value is None:
            return value
        return smart_text(value)

    def get_prep_value(self, value):
        # Emulate the functionality of other fields, which call to_python ...
        return self.to_python(value)

    def validate(self, value, model_instance):
        # quick sanity check that the file path is rooted.
        if value not in self.empty_values and not value.startswith(self.path):
            message = _('Value %(value)r does not start with %(path)r')
            raise ValidationError(message=message, code='invalid_choice',
                                  params={'value': value, 'path': self.path})

        # patch in an iterable of files based on the currently configured field.
        choices = tuple(self.formfield().choices)
        if value not in self.empty_values and choices:
            for option_key, option_value in choices:
                if option_key == value:
                    return
            message = _('Value %(value)r is not in %(choices)r')
            raise ValidationError(message=message, code='invalid_choice',
                                  params={'value': value, 'choices': choices})
        return super(StrictFilePathField, self).validate(
            value=value, model_instance=model_instance)

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


class StrictIntegerField(fields.IntegerField):
    default_validators = [
        MinValueValidator(-2147483648),
        MaxValueValidator(2147483647)
    ]

    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictIntegerField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictNullBooleanField(fields.NullBooleanField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictNullBooleanField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictPositiveIntegerField(fields.PositiveIntegerField):
    default_validators = [
        MinValueValidator(0),
        MaxValueValidator(2147483647)
    ]

    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictPositiveIntegerField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictPositiveSmallIntegerField(fields.PositiveSmallIntegerField):
    default_validators = [
        MinValueValidator(0),
        MaxValueValidator(32767)
    ]

    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictPositiveSmallIntegerField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictSlugField(fields.SlugField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictSlugField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictSmallIntegerField(fields.SmallIntegerField):
    default_validators = [
        MinValueValidator(-32768),
        MaxValueValidator(32767)
    ]

    def contribute_to_class(self, cls, name, **kwargs):
        super(StrictSmallIntegerField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, FieldCleaningDescriptor(self))


class StrictTextField(fields.TextField):
    def __init__(self, *args, **kwargs):
        super(StrictTextField, self).__init__(*args, **kwargs)
        if self.max_length is not None:
            self.validators.append(MaxLengthValidator(self.max_length))

    def to_python(self, value):
        # why the hell isn't this in Django?
        if isinstance(value, six.string_types) or value is None:
            return value
        return smart_text(value)

    def get_prep_value(self, value):
        # Emulate the functionality of other fields, which call to_python ...
        return self.to_python(value)

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
    fields.BinaryField
except AttributeError:
    class StrictBinaryField(object):
        __slots__ = ()
        def __init__(self):
            raise FieldError("Can't use StrictBinaryField because it's "
                             "superclass doesn't exist in the installed "
                             "version of Django")
else:
    class StrictBinaryField(fields.BinaryField):
        def contribute_to_class(self, cls, name, **kwargs):
            super(StrictBinaryField, self).contribute_to_class(cls, name, **kwargs)
            setattr(cls, self.name, FieldCleaningDescriptor(self))


try:
    from model_mommy import generators
except ImportError:  # model_mommy is not installed
    MODEL_MOMMY_MAPPING = {}
else:

    def gen_commaseparated_ingeters(max_length):
        return ','.join(str(generators.gen_integer(1, 9))
                        for x in six.moves.range(1, max_length // 2))
    gen_commaseparated_ingeters.required = ['max_length']

    MODEL_MOMMY_MAPPING = {
        StrictBooleanField: generators.gen_boolean,
        StrictBigIntegerField: generators.gen_integer,
        StrictCharField: generators.gen_string,
        StrictCommaSeparatedIntegerField: gen_commaseparated_ingeters,
        StrictDateField: generators.gen_date,
        StrictDateTimeField: generators.gen_datetime,
        StrictDecimalField: generators.gen_decimal,
        StrictEmailField: generators.gen_email,
        StrictTimeField: generators.gen_time,
        StrictSmallIntegerField: lambda: generators.gen_integer(-32768, 32767),
        StrictPositiveSmallIntegerField: lambda: generators.gen_integer(0, 32767),
        StrictIntegerField: lambda: generators.gen_integer(-2147483648, 2147483647),
        StrictPositiveIntegerField: lambda: generators.gen_integer(0, 2147483647),
        StrictURLField: generators.gen_url,
        StrictSlugField: generators.gen_slug,
        StrictFloatField: generators.gen_float,
        StrictTextField: generators.gen_text,
    }
