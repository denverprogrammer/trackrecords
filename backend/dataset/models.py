# Create your models here.

import os
import typing
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

from django.conf import settings
from django.db import models
from django.db.models.functions import Coalesce
from django.db.models.query import RawQuerySet


class ImportExportStub(object):
    columns = None
    tbl_name = None
    file_name = None
    download_url = None
    extract_folder = None
    extract_file = None

    def download_data_file(self) -> None:
        response = urlopen(self.download_url)
        zipfile = ZipFile(BytesIO(response.read()))
        zipfile.extractall(path=self.extract_folder)

    def remove_data_file(self) -> None:
        os.remove(self.file_name)

    def import_data(self) -> str:
        return f'''
            COPY {self.tbl_name}({self.columns})
            FROM '{self.file_name}'
            DELIMITER E'\t' CSV HEADER;
        '''

    def export_data(self) -> str:
        return f'''
            COPY (select {self.columns} from {self.tbl_name}) 
            TO '{self.file_name}' 
            WITH DELIMITER E'\t' CSV HEADER;
        '''


class TempSymbolQuerySet(models.QuerySet['TempSymbol']):
    def distinct_naics(self):
        return self.filter(naics__isnull=False)\
            .values('naics').distinct().order_by('naics')

    def distinct_sic(self):
        return self.filter(sic__isnull=False)\
            .values('sic').distinct().order_by('sic')

    def distinct_exchanges(self):
        return self.filter(exchange__isnull=False)\
            .values('exchange').distinct().order_by('exchange')

    def distinct_markets(self):
        return self.filter(listed_market__isnull=False)\
            .values('listed_market').distinct().order_by('listed_market')

    def distinct_securities(self):
        return self.filter(security_type__isnull=False)\
            .values('security_type').distinct().order_by('security_type')


class TempSymbolManager(models.Manager['TempSymbol'], ImportExportStub):

    columns = '''
        symbol,
        description,
        exchange,
        listed_market,
        security_type,
        sic,
        frontmonth,
        naics
    '''
    tbl_name = 'dataset_tempsymbol'
    download_url = 'https://www.iqfeed.net/downloads/download_file.cfm?type=mktsymbols'
    extract_folder = '/home/data/symbols'
    extract_file = '/mktsymbols_v2.txt'
    file_name = '/home/data/symbols/mktsymbols_v2.txt'

    def get_queryset(self) -> TempSymbolQuerySet:
        return TempSymbolQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> TempSymbolQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> TempSymbolQuerySet:
        return super().filter(*args, **kwargs)

    def clear_temp(self) -> str:
        return 'DELETE FROM dataset_tempsymbol;'

        # SELECT DISTINCT naics
        # FROM dataset_tempsymbol as temp
        # WHERE temp.naics IS NOT NULL

        # SELECT DISTINCT sic
        # FROM dataset_tempsymbol as temp
        # WHERE temp.sic IS NOT NULL

        # SELECT DISTINCT exchange
        # FROM dataset_tempsymbol as temp

        # SELECT DISTINCT listed_market
        # FROM dataset_tempsymbol as temp

        # SELECT DISTINCT security_type
        # FROM dataset_tempsymbol as temp

    def insert_symbols(self) -> str:
        return '''
            INSERT INTO dataset_symbol (
                code,
                description,
                exchange_id,
                market_id,
                security_id,
                sic_id,
                frontmonth,
                naics_id
            )
            SELECT
                DISTINCT temp.symbol, 
                temp.description, 
                exchanges.id, 
                markets.id, 
                securities.id, 
                COALESCE(sic_codes.id, NULL), 
                temp.frontmonth, 
                COALESCE(naics_codes.id, NULL)
            FROM
                dataset_tempsymbol as temp
            LEFT JOIN dataset_exchange exchanges
                ON temp.exchange = exchanges.code
            LEFT JOIN dataset_market markets
                ON temp.listed_market = markets.code
            LEFT JOIN dataset_security securities
                ON temp.security_type = securities.code
            LEFT JOIN dataset_naicscode naics_codes
                ON temp.naics = naics_codes.code
            LEFT JOIN dataset_siccode sic_codes
                ON temp.sic = sic_codes.code
            ON CONFLICT (code) DO NOTHING;
        '''


class NaicsManager(models.Manager, ImportExportStub):

    columns = 'code, description'
    tbl_name = 'dataset_naicscode'
    file_name = '/home/data/naics.tsv'

    def insert_from_data(self, query: models.QuerySet) -> str:
        return f'''
            INSERT INTO {self.tbl_name} (code)
            {query.query}
            ON CONFLICT (code) DO NOTHING;
        '''


class SicManager(models.Manager, ImportExportStub):

    columns = 'code, description'
    tbl_name = 'dataset_siccode'
    file_name = '/home/data/sic.tsv'

    def insert_from_data(self, query: models.QuerySet) -> str:
        return f'''
            INSERT INTO {self.tbl_name} (code)
            {query.query}
            ON CONFLICT (code) DO NOTHING;
        '''


class ExchangeManager(models.Manager, ImportExportStub):

    columns = 'code, description'
    tbl_name = 'dataset_exchange'
    file_name = '/home/data/exchange.tsv'

    def insert_from_data(self, query: models.QuerySet) -> str:
        return f'''
            INSERT INTO {self.tbl_name} (code)
            {query.query}
            ON CONFLICT (code) DO NOTHING;
        '''


class MarketManager(models.Manager, ImportExportStub):

    columns = 'code, description'
    tbl_name = 'dataset_market'
    file_name = '/home/data/market.tsv'

    def insert_from_data(self, query: models.QuerySet) -> str:
        return f'''
            INSERT INTO {self.tbl_name} (code)
            {query.query}
            ON CONFLICT (code) DO NOTHING;
        '''


class SecurityManager(models.Manager, ImportExportStub):

    columns = 'code, description'
    tbl_name = 'dataset_security'
    file_name = '/home/data/security.tsv'

    def insert_from_data(self, query: models.QuerySet) -> str:
        return f'''
            INSERT INTO {self.tbl_name} (code)
            {query.query}
            ON CONFLICT (code) DO NOTHING;
        '''


class CodeStub(models.Model):
    code = models.CharField(max_length=32, unique=True)

    description = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['code']

    def __str__(self):
        return self.code


class NaicsCode(CodeStub):

    objects: NaicsManager = NaicsManager()


class SicCode(CodeStub):

    objects: SicManager = SicManager()


class Exchange(CodeStub):

    objects: ExchangeManager = ExchangeManager()


class Market(CodeStub):

    objects: MarketManager = MarketManager()


class Security(CodeStub):

    objects: SecurityManager = SecurityManager()

    class Meta(CodeStub.Meta):
        verbose_name_plural = 'securities'


class Symbol(CodeStub):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)

    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    security = models.ForeignKey(Security, on_delete=models.CASCADE)

    sic = models.ForeignKey(
        SicCode, on_delete=models.CASCADE, null=True, blank=True)

    frontmonth = models.CharField(max_length=1, null=True, blank=True)

    naics = models.ForeignKey(
        NaicsCode, on_delete=models.CASCADE, null=True, blank=True)

    class Meta(CodeStub.Meta):
        ordering = ['exchange__code', 'code']

    def __str__(self):
        return "(%s):%s" % (self.exchange.code, self.code)


class TempSymbol(models.Model):
    symbol = models.CharField(max_length=32, null=True, blank=True)

    description = models.CharField(max_length=150, null=True, blank=True)

    exchange = models.CharField(max_length=16, null=True, blank=True)

    listed_market = models.CharField(max_length=16, null=True, blank=True)

    security_type = models.CharField(max_length=16, null=True, blank=True)

    sic = models.CharField(max_length=8, null=True, blank=True)

    frontmonth = models.CharField(max_length=1, null=True, blank=True)

    naics = models.CharField(max_length=16, null=True, blank=True)

    objects: TempSymbolManager = TempSymbolManager()

    class Meta(CodeStub.Meta):
        ordering = ['symbol']

    def __str__(self):
        return "(%s):%s" % (self.symbol)

# SELECT DISTINCT exchange, COUNT(exchange) as count
# FROM dataset_tempsymbol
# GROUP BY exchange
# ORDER BY count DESC
# LIMIT 1000

    # def with_counts(self):
    #     return self.annotate(
    #         num_responses=Coalesce(models.Count("response"), 0)
    #     )
