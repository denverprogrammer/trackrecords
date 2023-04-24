from django import forms
from django.contrib.postgres.fields import ArrayField


class ArraySelectMultiple(forms.SelectMultiple):

    def value_omitted_from_data(self, data, files, name):
        return False


class ChoiceArrayField(ArrayField):

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.TypedMultipleChoiceField,
            'choices': self.base_field.choices,
            'coerce': self.base_field.to_python,
            'widget': ArraySelectMultiple
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't care for it.
        # pylint:disable=bad-super-call
        return super(ArrayField, self).formfield(**defaults)
