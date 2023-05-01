
import os
import typing
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

from core import constants
from core.forms import ChoiceArrayField
from core.models._models import (
    _Exchange,
    _Market,
    _NaicsCode,
    _Order,
    _Permission,
    _Portfolio,
    _Position,
    _Security,
    _SicCode,
    _Subscription,
    _Symbol,
    _TempSymbol,
)
from django.conf import settings
from django.db import models
from django.db.backends.utils import CursorWrapper


class PositionQuerySet(models.QuerySet[_Position]):
    pass


class OrderQuerySet(models.QuerySet[_Order]):
    pass


class PermissionQuerySet(models.QuerySet[_Permission]):
    pass


class PortfolioQuerySet(models.QuerySet[_Portfolio]):
    pass


class SubscriptionQuerySet(models.QuerySet[_Subscription]):
    pass


class SymbolQuerySet(models.QuerySet[_Symbol]):
    pass


class TempSymbolQuerySet(models.QuerySet[_TempSymbol]):

    def distinct_symbols(self):
        sql = '''
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
        '''

        return self.raw(sql.strip())

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
