
import os
import typing
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

from core import constants
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
from core.models._querysets import (
    OrderQuerySet,
    PermissionQuerySet,
    PortfolioQuerySet,
    PositionQuerySet,
    SubscriptionQuerySet,
    SymbolQuerySet,
    TempSymbolQuerySet,
)
from django.conf import settings
from django.db import models
from django.db.backends.utils import CursorWrapper


class ImportExportStub(object):
    import_columns = []
    insert_columns = []
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

    def get_import_columns(self) -> str:
        return ', '.join(self.import_columns)

    def get_insert_columns(self) -> str:
        return ', '.join(self.insert_columns)

    def import_from_file(self, cursor: CursorWrapper) -> None:
        sql = f'''
            COPY {self.tbl_name} ({self.get_import_columns()})
            FROM '{self.file_name}'
            DELIMITER E'\t' CSV HEADER;
        '''

        cursor.execute(sql)

    def export_to_file(self, cursor: CursorWrapper) -> None:
        sql = f'''
            COPY (select {self.get_import_columns()} from {self.tbl_name})
            TO '{self.file_name}'
            WITH DELIMITER E'\t' CSV HEADER;
        '''

        cursor.execute(sql)

    def insert_from_temp(self, cursor: CursorWrapper, query: models.QuerySet) -> None:
        sql = f'''
            INSERT INTO {self.tbl_name} ({self.get_insert_columns()})
            {query.query}
            ON CONFLICT ({self.insert_columns[0]}) DO NOTHING;
        '''

        cursor.execute(sql)

    def clear_table(self, cursor: CursorWrapper) -> str:
        cursor.execute(f'DELETE FROM {self.tbl_name};')


class PermissionManager(models.Manager[_Permission]):

    def default_owner_permissions(self, portfolio: _Portfolio):
        items = []

        # Portfolio owner permissions
        items.append(self.create(
            collection=constants.CollectionName.PORTFOLIO,
            group=constants.CollectionGroup.PORTFOLIOS,
            role=constants.RoleType.OWNER,
            actions=constants.NO_CREATE_ACTIONS,
            portfolio=portfolio
        ))

        # Permission owner permissions
        items.append(self.create(
            collection=constants.CollectionName.PERMISSION,
            group=constants.CollectionGroup.PERMISSIONS,
            role=constants.RoleType.OWNER,
            actions=constants.NO_CREATE_OR_DELETE_ACTIONS,
            portfolio=portfolio
        ))

        # Subscription owner permissions
        items.append(self.create(
            collection=constants.CollectionName.SUBSCRIPTION,
            group=constants.CollectionGroup.SUBSCRIPTIONS,
            role=constants.RoleType.OWNER,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        # Position owner permissions
        items.append(self.create(
            collection=constants.CollectionName.OPEN_POSITION,
            group=constants.CollectionGroup.POSITIONS,
            role=constants.RoleType.OWNER,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.CLOSED_POSITION,
            group=constants.CollectionGroup.POSITIONS,
            role=constants.RoleType.OWNER,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        # Order order permissions
        items.append(self.create(
            collection=constants.CollectionName.FILLED_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.OWNER,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.PARTIAL_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.OWNER,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.PENDING_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.OWNER,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.CANCELLED_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.OWNER,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        return items

    def default_admin_permissions(self, portfolio: _Portfolio):
        items = []

        # Portfolio admin permissions
        items.append(self.create(
            collection=constants.CollectionName.PORTFOLIO,
            group=constants.CollectionGroup.PORTFOLIOS,
            role=constants.RoleType.ADMIN,
            actions=constants.NO_CREATE_OR_DELETE_ACTIONS,
            portfolio=portfolio
        ))

        # Permission admin permissions
        items.append(self.create(
            collection=constants.CollectionName.PERMISSION,
            group=constants.CollectionGroup.PERMISSIONS,
            role=constants.RoleType.ADMIN,
            actions=constants.NO_CREATE_OR_DELETE_ACTIONS,
            portfolio=portfolio
        ))

        # Subscription admin permissions
        items.append(self.create(
            collection=constants.CollectionName.SUBSCRIPTION,
            group=constants.CollectionGroup.SUBSCRIPTIONS,
            role=constants.RoleType.ADMIN,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        # Position admin permissions
        items.append(self.create(
            collection=constants.CollectionName.OPEN_POSITION,
            group=constants.CollectionGroup.POSITIONS,
            role=constants.RoleType.ADMIN,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.CLOSED_POSITION,
            group=constants.CollectionGroup.POSITIONS,
            role=constants.RoleType.ADMIN,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        # Order admin permissions
        items.append(self.create(
            collection=constants.CollectionName.FILLED_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.ADMIN,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.PARTIAL_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.ADMIN,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.PENDING_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.ADMIN,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.CANCELLED_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.ADMIN,
            actions=constants.ALL_ACTIONS,
            portfolio=portfolio
        ))

        return items

    def default_subscription_permissions(self, portfolio: _Portfolio):
        items = []

        # Portfolio subscriber permissions
        items.append(self.create(
            collection=constants.CollectionName.PORTFOLIO,
            group=constants.CollectionGroup.PORTFOLIOS,
            role=constants.RoleType.SUBSCRIBER,
            actions=constants.READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        # Permission subscriber permissions
        items.append(self.create(
            collection=constants.CollectionName.PERMISSION,
            group=constants.CollectionGroup.PERMISSIONS,
            role=constants.RoleType.SUBSCRIBER,
            actions=constants.READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        # Subscription subscriber permissions
        items.append(self.create(
            collection=constants.CollectionName.SUBSCRIPTION,
            group=constants.CollectionGroup.SUBSCRIPTIONS,
            role=constants.RoleType.SUBSCRIBER,
            actions=constants.NO_ACTIONS,
            portfolio=portfolio
        ))

        # Position subscriber permissions
        items.append(self.create(
            collection=constants.CollectionName.OPEN_POSITION,
            group=constants.CollectionGroup.POSITIONS,
            role=constants.RoleType.SUBSCRIBER,
            actions=constants.READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.CLOSED_POSITION,
            group=constants.CollectionGroup.POSITIONS,
            role=constants.RoleType.SUBSCRIBER,
            actions=constants.READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        # Order subscriber permissions
        items.append(self.create(
            collection=constants.CollectionName.FILLED_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.SUBSCRIBER,
            actions=constants.READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.PARTIAL_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.SUBSCRIBER,
            actions=constants.READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.PENDING_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.SUBSCRIBER,
            actions=constants.READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.CANCELLED_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.SUBSCRIBER,
            actions=constants.READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        return items

    def default_guest_permissions(self, portfolio: _Portfolio):
        items = []

        # Portfolio guest permissions
        items.append(self.create(
            collection=constants.CollectionName.PORTFOLIO,
            group=constants.CollectionGroup.PORTFOLIOS,
            role=constants.RoleType.GUEST,
            actions=constants.READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        # Permission guest permissions
        items.append(self.create(
            collection=constants.CollectionName.PERMISSION,
            group=constants.CollectionGroup.PERMISSIONS,
            role=constants.RoleType.GUEST,
            actions=constants.READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        # Subscription guest permissions
        items.append(self.create(
            collection=constants.CollectionName.SUBSCRIPTION,
            group=constants.CollectionGroup.SUBSCRIPTIONS,
            role=constants.RoleType.GUEST,
            actions=constants.NO_ACTIONS,
            portfolio=portfolio
        ))

        # Position guest permissions
        items.append(self.create(
            collection=constants.CollectionName.OPEN_POSITION,
            group=constants.CollectionGroup.POSITIONS,
            role=constants.RoleType.GUEST,
            actions=constants.NO_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.CLOSED_POSITION,
            group=constants.CollectionGroup.POSITIONS,
            role=constants.RoleType.GUEST,
            actions=constants.NO_ACTIONS,
            portfolio=portfolio
        ))

        # Order guest permissions
        items.append(self.create(
            collection=constants.CollectionName.FILLED_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.GUEST,
            actions=constants.NO_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.PARTIAL_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.GUEST,
            actions=constants.NO_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.PENDING_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.GUEST,
            actions=constants.NO_ACTIONS,
            portfolio=portfolio
        ))

        items.append(self.create(
            collection=constants.CollectionName.CANCELLED_ORDER,
            group=constants.CollectionGroup.ORDERS,
            role=constants.RoleType.GUEST,
            actions=constants.NO_ACTIONS,
            portfolio=portfolio
        ))

        return items

    def get_queryset(self) -> PermissionQuerySet:
        return PermissionQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> PermissionQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> PermissionQuerySet:
        return super().filter(*args, **kwargs)


class PortfolioManager(models.Manager[_Portfolio]):

    def get_queryset(self) -> PortfolioQuerySet:
        return PortfolioQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> PortfolioQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> PortfolioQuerySet:
        return super().filter(*args, **kwargs)


class SubscriptionManager(models.Manager[_Subscription]):

    def get_queryset(self) -> SubscriptionQuerySet:
        return SubscriptionQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> SubscriptionQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> SubscriptionQuerySet:
        return super().filter(*args, **kwargs)


class SymbolManager(models.Manager[_Symbol], ImportExportStub):

    insert_columns = [
        'code',
        'description',
        'exchange_id',
        'market_id',
        'security_id',
        'sic_id',
        'frontmonth',
        'naics_id'
    ]
    tbl_name = 'dataset_symbol'

    def get_queryset(self) -> SymbolQuerySet:
        return SymbolQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> SymbolQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> SymbolQuerySet:
        return super().filter(*args, **kwargs)


class TempSymbolManager(models.Manager[_TempSymbol], ImportExportStub):

    import_columns = [
        'symbol',
        'description',
        'exchange',
        'listed_market',
        'security_type',
        'sic',
        'frontmonth',
        'naics'
    ]
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


class NaicsManager(models.Manager[_NaicsCode], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    tbl_name = 'dataset_naicscode'
    file_name = '/home/data/naics.tsv'


class SicManager(models.Manager[_SicCode], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    tbl_name = 'dataset_siccode'
    file_name = '/home/data/sic.tsv'


class ExchangeManager(models.Manager[_Exchange], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    tbl_name = 'dataset_exchange'
    file_name = '/home/data/exchange.tsv'


class MarketManager(models.Manager[_Market], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    tbl_name = 'dataset_market'
    file_name = '/home/data/market.tsv'


class SecurityManager(models.Manager[_Security], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    tbl_name = 'dataset_security'
    file_name = '/home/data/security.tsv'


class OrderManager(models.Manager[_Order]):

    def get_queryset(self) -> OrderQuerySet:
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> OrderQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> OrderQuerySet:
        return super().filter(*args, **kwargs)


class PositionManager(models.Manager[_Position]):

    def get_queryset(self) -> PositionQuerySet:
        return PositionQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> PositionQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> PositionQuerySet:
        return super().filter(*args, **kwargs)
