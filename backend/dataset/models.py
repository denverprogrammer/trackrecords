# Create your models here.
from django.conf import settings
from django.db import models


class AbstractName(models.Model):
    short_name = models.CharField(max_length=32, db_index=True, unique=True)

    long_name = models.CharField(max_length=150, null=True, blank=True)

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

    sic = models.CharField(max_length=8, null=True, blank=True)

    frontmonth = models.CharField(max_length=1, null=True, blank=True)

    naics = models.CharField(max_length=16, null=True, blank=True)

    class Meta(AbstractName.Meta):
        ordering = ['exchange__short_name', 'short_name']

    def __str__(self):
        return "(%s):%s" % (self.exchange.short_name, self.short_name)


class TempSymbol(models.Model):
    symbol = models.CharField(max_length=32, null=True, blank=True)

    description = models.CharField(max_length=150, null=True, blank=True)

    exchange = models.CharField(max_length=16, null=True, blank=True)

    listed_market = models.CharField(max_length=16, null=True, blank=True)

    security_type = models.CharField(max_length=16, null=True, blank=True)

    sic = models.CharField(max_length=8, null=True, blank=True)

    frontmonth = models.CharField(max_length=1, null=True, blank=True)

    naics = models.CharField(max_length=16, null=True, blank=True)

    class Meta(AbstractName.Meta):
        ordering = ['exchange', 'symbol']

    def __str__(self):
        return "(%s):%s" % (self.exchange, self.symbol)

# SELECT DISTINCT exchange, COUNT(exchange) as count
# FROM dataset_tempsymbol
# GROUP BY exchange
# ORDER BY count DESC
# LIMIT 1000

# INSERT INTO dataset_exchange (short_name)
# SELECT DISTINCT exchange FROM dataset_tempsymbol as temp
# GROUP BY temp.exchange
# ON CONFLICT (short_name) DO NOTHING;

# INSERT INTO dataset_market (short_name)
# SELECT DISTINCT listed_market FROM dataset_tempsymbol as temp
# GROUP BY temp.listed_market
# ON CONFLICT (short_name) DO NOTHING;

# INSERT INTO dataset_security (short_name)
# SELECT DISTINCT security_type FROM dataset_tempsymbol as temp
# GROUP BY temp.security_type
# ON CONFLICT (short_name) DO NOTHING;

# INSERT INTO dataset_symbol (
#    short_name,
#    long_name,
#    exchange_id,
#    market_id,
#    security_id,
#    sic,
#    frontmonth,
#    naics
# )
# SELECT DISTINCT symbol, description, tblExchanges.id, tblMarkets.id, tblSecurities.id, sic, frontmonth, naics
# FROM dataset_tempsymbol as temp, dataset_exchange as tblExchanges, dataset_market as tblMarkets, dataset_security as tblSecurities
# WHERE temp.exchange = tblExchanges.short_name AND temp.listed_market = tblMarkets.short_name AND temp.security_type = tblSecurities.short_name
# ON CONFLICT (short_name) DO NOTHING;
