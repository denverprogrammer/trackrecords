from core import constants
from core.forms import ChoiceArrayField
from django.db import models


class _CodeStub(models.Model):

    code = models.CharField(max_length=32, unique=True)

    description = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        ordering = ['code']
        abstract = True

    def __str__(self):
        return self.code
