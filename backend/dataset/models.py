# Create your models here.
from django.conf import settings
from django.db import models


class AbstractName(models.Model):
    short_name = models.CharField(max_length=32, db_index=True)

    long_name = models.CharField(max_length=64)

    class Meta:
        abstract = True
        ordering = ['short_name']

    def __str__(self):
        return self.short_name


class Exchange(AbstractName):
    pass


class Market(AbstractName):
    pass


class Security(AbstractName):

    class Meta(AbstractName.Meta):
        verbose_name_plural = 'securities'


class Symbol(AbstractName):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)

    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    security = models.ForeignKey(Security, on_delete=models.CASCADE)

    class Meta(AbstractName.Meta):
        ordering = ['exchange__short_name', 'short_name']

    def __str__(self):
        return "(%s):%s" % (self.exchange.short_name, self.short_name)
