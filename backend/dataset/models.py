# Create your models here.

import os
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


class TempSymbolManager(models.Manager, ImportExportStub):

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
    file_name = extract_folder . extract_file

    def clear_temp(self) -> str:
        return 'DELETE FROM dataset_tempsymbol;'

    def insert_naics(self) -> str:
        return '''
            INSERT INTO dataset_naicscode (code)
            SELECT DISTINCT naics 
            FROM dataset_tempsymbol as temp
            WHERE temp.naics IS NOT NULL
            ON CONFLICT (code) DO NOTHING;
        '''

    def insert_sic(self) -> str:
        return '''
            INSERT INTO dataset_siccode (code)
            SELECT DISTINCT sic 
            FROM dataset_tempsymbol as temp
            WHERE temp.sic IS NOT NULL
            ON CONFLICT (code) DO NOTHING;
        '''

    def insert_exchanges(self) -> str:
        return '''
            INSERT INTO dataset_exchange (code)
            SELECT DISTINCT exchange 
            FROM dataset_tempsymbol as temp
            ON CONFLICT (code) DO NOTHING;
        '''

    def insert_markets(self) -> str:
        return '''
            INSERT INTO dataset_market (code)
            SELECT DISTINCT listed_market 
            FROM dataset_tempsymbol as temp
            ON CONFLICT (code) DO NOTHING;
        '''

    def insert_securities(self) -> str:
        return '''
            INSERT INTO dataset_security (code)
            SELECT DISTINCT security_type 
            FROM dataset_tempsymbol as temp
            ON CONFLICT (code) DO NOTHING;
        '''

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


class SicManager(models.Manager, ImportExportStub):

    columns = 'code, description'
    tbl_name = 'dataset_siccode'
    file_name = '/home/data/sic.tsv'


class ExchangeManager(models.Manager, ImportExportStub):

    columns = 'code, description'
    tbl_name = 'dataset_exchange'
    file_name = '/home/data/exchange.tsv'


class MarketManager(models.Manager, ImportExportStub):

    columns = 'code, description'
    tbl_name = 'dataset_market'
    file_name = '/home/data/market.tsv'


class SecurityManager(models.Manager, ImportExportStub):

    columns = 'code, description'
    tbl_name = 'dataset_security'
    file_name = '/home/data/security.tsv'


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
    pass


class Security(CodeStub):

    objects: SecurityManager = SecurityManager()

    class Meta(AbstractName.Meta):
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

    class Meta(AbstractName.Meta):
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

    class Meta(AbstractName.Meta):
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
