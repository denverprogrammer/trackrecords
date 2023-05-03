
import typing

from core import constants
from core.models._ManagerStubs import ImportExportStub
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
    ExchangeQuerySet,
    MarketQuerySet,
    NaicsQuerySet,
    OrderQuerySet,
    PermissionQuerySet,
    PortfolioQuerySet,
    PositionQuerySet,
    SecurityQuerySet,
    SicQuerySet,
    SubscriptionQuerySet,
    SymbolQuerySet,
    TempSymbolQuerySet,
)
from django.db import models


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

    def calculate(self) -> None:
        pass

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
    file_name = '/home/data/naics.tsv'

    def get_queryset(self) -> NaicsQuerySet:
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> NaicsQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> NaicsQuerySet:
        return super().filter(*args, **kwargs)


class SicManager(models.Manager[_SicCode], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    file_name = '/home/data/sic.tsv'

    def get_queryset(self) -> SicQuerySet:
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> SicQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> SicQuerySet:
        return super().filter(*args, **kwargs)


class ExchangeManager(models.Manager[_Exchange], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    file_name = '/home/data/exchange.tsv'

    def get_queryset(self) -> ExchangeQuerySet:
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> ExchangeQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> ExchangeQuerySet:
        return super().filter(*args, **kwargs)


class MarketManager(models.Manager[_Market], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    file_name = '/home/data/market.tsv'

    def get_queryset(self) -> MarketQuerySet:
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> MarketQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> MarketQuerySet:
        return super().filter(*args, **kwargs)


class SecurityManager(models.Manager[_Security], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    file_name = '/home/data/security.tsv'

    def get_queryset(self) -> SecurityQuerySet:
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> SecurityQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> SecurityQuerySet:
        return super().filter(*args, **kwargs)


class OrderManager(models.Manager[_Order]):

    def get_queryset(self) -> OrderQuerySet:
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> OrderQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> OrderQuerySet:
        return super().filter(*args, **kwargs)


class PositionManager(models.Manager[_Position]):

    def calculate(self) -> None:
        orders: OrderQuerySet = getattr(self.model, 'orders')

        for item in orders.sort_executed():
            pass

    def get_queryset(self) -> PositionQuerySet:
        return PositionQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> PositionQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> PositionQuerySet:
        return super().filter(*args, **kwargs)
