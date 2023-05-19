
import datetime
import typing

from core import constants
from core.models._ManagerStubs import ImportExportStub
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
from core.models.Abstractions import (
    AbstractExchange,
    AbstractMarket,
    AbstractNaicsCode,
    AbstractOrder,
    AbstractPermission,
    AbstractPortfolio,
    AbstractPosition,
    AbstractSecurity,
    AbstractSicCode,
    AbstractSubscription,
    AbstractSymbol,
    AbstractTempSymbol,
)
from django.db import models


class PermissionManager(models.Manager[AbstractPermission]):

    def default_owner_permissions(self, portfolio: AbstractPortfolio):
        items = []

        # Portfolio owner permissions
        items.append(self.create(
            collection=constants.CollectionName.PORTFOLIO,
            group=constants.CollectionGroup.PORTFOLIOS,
            role=constants.RoleType.OWNER,
            actions=constants.ALL_ACTIONS,
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

    def default_admin_permissions(self, portfolio: AbstractPortfolio):
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

    def default_subscription_permissions(self, portfolio: AbstractPortfolio):
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

    def default_guest_permissions(self, portfolio: AbstractPortfolio):
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


class PortfolioManager(models.Manager[AbstractPortfolio]):

    def update_stats(self, portfolio: AbstractPortfolio) -> None:
        positions: PositionQuerySet = getattr(portfolio, 'positions')

        first_order = None

        entry_stamp = None
        entry_amount = 0
        entry_price = 0
        entry_count = 0

        exit_stamp = None
        exit_amount = 0
        exit_price = 0
        exit_count = 0

        for item in positions:
            pass

    def get_queryset(self) -> PortfolioQuerySet:
        return PortfolioQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> PortfolioQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> PortfolioQuerySet:
        return super().filter(*args, **kwargs)


class SubscriptionManager(models.Manager[AbstractSubscription]):

    def get_queryset(self) -> SubscriptionQuerySet:
        return SubscriptionQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> SubscriptionQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> SubscriptionQuerySet:
        return super().filter(*args, **kwargs)


class SymbolManager(models.Manager[AbstractSymbol], ImportExportStub):

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


class TempSymbolManager(models.Manager[AbstractTempSymbol], ImportExportStub):

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


class NaicsManager(models.Manager[AbstractNaicsCode], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    file_name = '/home/data/naics.tsv'

    def get_queryset(self) -> NaicsQuerySet:
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> NaicsQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> NaicsQuerySet:
        return super().filter(*args, **kwargs)


class SicManager(models.Manager[AbstractSicCode], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    file_name = '/home/data/sic.tsv'

    def get_queryset(self) -> SicQuerySet:
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> SicQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> SicQuerySet:
        return super().filter(*args, **kwargs)


class ExchangeManager(models.Manager[AbstractExchange], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    file_name = '/home/data/exchange.tsv'

    def get_queryset(self) -> ExchangeQuerySet:
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> ExchangeQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> ExchangeQuerySet:
        return super().filter(*args, **kwargs)


class MarketManager(models.Manager[AbstractMarket], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    file_name = '/home/data/market.tsv'

    def get_queryset(self) -> MarketQuerySet:
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> MarketQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> MarketQuerySet:
        return super().filter(*args, **kwargs)


class SecurityManager(models.Manager[AbstractSecurity], ImportExportStub):

    insert_columns = ['code']
    import_columns = ['code', 'description']
    file_name = '/home/data/security.tsv'

    def get_queryset(self) -> SecurityQuerySet:
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> SecurityQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> SecurityQuerySet:
        return super().filter(*args, **kwargs)


class OrderManager(models.Manager[AbstractOrder]):

    def get_queryset(self) -> OrderQuerySet:
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> OrderQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> OrderQuerySet:
        return super().filter(*args, **kwargs)

    def update_status(self, order: AbstractOrder) -> None:
        if order.order_status == constants.OrderStatus.CANCELLED:
            pass
        elif order.filled_amount is None and order.sent_amount > 0:
            order.order_status = constants.OrderStatus.PENDING
        elif order.filled_amount > 0 and order.filled_amount < order.sent_amount:
            order.order_status = constants.OrderStatus.PARTIAL
        elif order.filled_amount == order.sent_amount:
            order.order_status = constants.OrderStatus.FILLED


class PositionManager(models.Manager[AbstractPosition]):

    def update_status(self, position: AbstractPosition) -> None:
        orders: OrderQuerySet = getattr(position, 'orders')

        first_order = None

        entry_stamp = None
        entry_amount = 0
        entry_price = 0
        entry_count = 0
        entry_fees = 0

        exit_stamp = None
        exit_amount = 0
        exit_price = 0
        exit_count = 0
        exit_fees = 0
        price_difference = 0

        for item in orders.all():
            if item.hasAmount() == False:
                continue
            elif first_order is None:
                first_order = item
                entry_stamp = item.filled_stamp

            if item.order_action == first_order.order_action:
                entry_amount += item.filled_amount if item.filled_amount else 0
                entry_price += item.filled_price if item.filled_price else 0
                entry_fees += item.fees if item.fees else 0
                entry_count += 1
            else:
                exit_stamp = item.filled_stamp
                exit_amount += item.filled_amount if item.filled_amount else 0
                exit_price += item.filled_price if item.filled_price else 0
                exit_fees += item.fees if item.fees else 0
                exit_count += 1

        if entry_stamp:
            position.entry_stamp = entry_stamp
            position.entry_price = entry_price / entry_count
            position.entry_amount = entry_amount
            position.entry_fees = entry_fees
        else:
            position.entry_stamp = None
            position.entry_price = None
            position.entry_amount = None
            position.entry_fees = None

        if exit_stamp:
            position.exit_stamp = exit_stamp
            position.exit_price = exit_price / exit_count
            position.exit_amount = exit_amount
            position.exit_fees = exit_fees
        else:
            position.exit_stamp = None
            position.exit_price = None
            position.exit_amount = None
            position.exit_fees = None

        if first_order.order_action == constants.OrderAction.BUY:
            position.trend_type = constants.TrendType.LONG
        elif first_order.order_action == constants.OrderAction.SELL:
            position.trend_type = constants.TrendType.SHORT

        price_difference = abs(exit_price - entry_price)

        if exit_amount > 0:
            position.real_pnl = price_difference * exit_amount
        else:
            position.real_pnl = 0

        if entry_amount == exit_amount and exit_amount > 0:
            position.duration = exit_stamp - entry_stamp
        elif entry_amount > 0 and exit_amount == 0:
            tz_info = entry_stamp.tzinfo
            position.duration = datetime.datetime.now(tz_info) - entry_stamp
        else:
            position.duration = None

        if entry_amount > exit_amount and exit_amount > 0:
            position.unreal_pnl = entry_price * (entry_amount - exit_amount)
        elif entry_amount > exit_amount and exit_amount == 0:
            position.unreal_pnl = entry_price * entry_amount
        else:
            position.unreal_pnl = 0

        if entry_amount == exit_amount and exit_amount > 0:
            position.position_status = constants.PositionStatus.CLOSED
        else:
            position.position_status = constants.PositionStatus.OPEN

    def set_position(self, oder: AbstractOrder) -> None:
        oder.position = self.all().open_position_by(
            oder.portfolio.id,
            oder.symbol.id
        )

        if oder.position is None:
            oder.position = self.model()
            oder.position.portfolio = oder.portfolio
            oder.position.symbol = oder.symbol
            oder.position.entry_stamp = oder.sent_stamp
            oder.position.entry_price = oder.sent_price
            oder.position.entry_amount = oder.sent_amount
            oder.position.save()

    def get_queryset(self) -> PositionQuerySet:
        return PositionQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> PositionQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> PositionQuerySet:
        return super().filter(*args, **kwargs)
