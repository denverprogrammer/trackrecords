from typing import Any

from django import forms
from django.contrib.postgres.fields import ArrayField  # ✅ Correct import


class ArraySelectMultiple(forms.SelectMultiple):
    def value_omitted_from_data(self, data, files, name):
        return False


class ChoiceArrayField(ArrayField):  # type: ignore # ✅ Use Any to prevent type errors
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.TypedMultipleChoiceField,
            "choices": getattr(self.base_field, "choices", []),  # ✅ Avoid AttributeError
            "coerce": getattr(self.base_field, "to_python", str),  # ✅ Safer access
            "widget": ArraySelectMultiple,
        }
        defaults.update(kwargs)

        return super().formfield(**defaults)  # ✅ Correct `super()` call
