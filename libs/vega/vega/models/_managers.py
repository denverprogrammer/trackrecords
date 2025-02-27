import datetime

from django.db import models

# from django_cte import CTEManager, CTEQuerySet
from vega import constants
from vega.models._ManagerStubs import ImportExportStub
from vega.models._querysets import (
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
from vega.models.Abstractions import (
    AbstractExchangeType,
    AbstractMarketType,
    AbstractNaicsCodeType,
    AbstractOrder,
    AbstractOrderType,
    AbstractPermissionType,
    AbstractPortfolio,
    AbstractPortfolioType,
    AbstractPosition,
    AbstractPositionType,
    AbstractSecurityType,
    AbstractSicCodeType,
    AbstractSubscriptionType,
    AbstractSymbolType,
    AbstractTempSymbolType,
)

# import pprint


# from django.db.models import OuterRef, Subquery


class PermissionManager(models.Manager[AbstractPermissionType]):

    def default_owner_permissions(self, portfolio: AbstractPortfolio):
        items = []

        # Portfolio owner permissions
        items.append(
            self.create(
                collection=constants.CollectionName.PORTFOLIO,
                group=constants.CollectionGroup.PORTFOLIOS,
                role=constants.RoleType.OWNER,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Permission owner permissions
        items.append(
            self.create(
                collection=constants.CollectionName.PERMISSION,
                group=constants.CollectionGroup.PERMISSIONS,
                role=constants.RoleType.OWNER,
                actions=constants.NO_CREATE_OR_DELETE_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Subscription owner permissions
        items.append(
            self.create(
                collection=constants.CollectionName.SUBSCRIPTION,
                group=constants.CollectionGroup.SUBSCRIPTIONS,
                role=constants.RoleType.OWNER,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Position owner permissions
        items.append(
            self.create(
                collection=constants.CollectionName.OPEN_POSITION,
                group=constants.CollectionGroup.POSITIONS,
                role=constants.RoleType.OWNER,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.CLOSED_POSITION,
                group=constants.CollectionGroup.POSITIONS,
                role=constants.RoleType.OWNER,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Order order permissions
        items.append(
            self.create(
                collection=constants.CollectionName.FILLED_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.OWNER,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.PARTIAL_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.OWNER,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.PENDING_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.OWNER,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.CANCELLED_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.OWNER,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        return items

    def default_admin_permissions(self, portfolio: AbstractPortfolio):
        items = []

        # Portfolio admin permissions
        items.append(
            self.create(
                collection=constants.CollectionName.PORTFOLIO,
                group=constants.CollectionGroup.PORTFOLIOS,
                role=constants.RoleType.ADMIN,
                actions=constants.NO_CREATE_OR_DELETE_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Permission admin permissions
        items.append(
            self.create(
                collection=constants.CollectionName.PERMISSION,
                group=constants.CollectionGroup.PERMISSIONS,
                role=constants.RoleType.ADMIN,
                actions=constants.NO_CREATE_OR_DELETE_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Subscription admin permissions
        items.append(
            self.create(
                collection=constants.CollectionName.SUBSCRIPTION,
                group=constants.CollectionGroup.SUBSCRIPTIONS,
                role=constants.RoleType.ADMIN,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Position admin permissions
        items.append(
            self.create(
                collection=constants.CollectionName.OPEN_POSITION,
                group=constants.CollectionGroup.POSITIONS,
                role=constants.RoleType.ADMIN,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.CLOSED_POSITION,
                group=constants.CollectionGroup.POSITIONS,
                role=constants.RoleType.ADMIN,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Order admin permissions
        items.append(
            self.create(
                collection=constants.CollectionName.FILLED_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.ADMIN,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.PARTIAL_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.ADMIN,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.PENDING_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.ADMIN,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.CANCELLED_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.ADMIN,
                actions=constants.ALL_ACTIONS,
                portfolio=portfolio,
            )
        )

        return items

    def default_subscription_permissions(self, portfolio: AbstractPortfolio):
        items = []

        # Portfolio subscriber permissions
        items.append(
            self.create(
                collection=constants.CollectionName.PORTFOLIO,
                group=constants.CollectionGroup.PORTFOLIOS,
                role=constants.RoleType.SUBSCRIBER,
                actions=constants.READ_ONLY_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Permission subscriber permissions
        items.append(
            self.create(
                collection=constants.CollectionName.PERMISSION,
                group=constants.CollectionGroup.PERMISSIONS,
                role=constants.RoleType.SUBSCRIBER,
                actions=constants.READ_ONLY_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Subscription subscriber permissions
        items.append(
            self.create(
                collection=constants.CollectionName.SUBSCRIPTION,
                group=constants.CollectionGroup.SUBSCRIPTIONS,
                role=constants.RoleType.SUBSCRIBER,
                actions=constants.NO_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Position subscriber permissions
        items.append(
            self.create(
                collection=constants.CollectionName.OPEN_POSITION,
                group=constants.CollectionGroup.POSITIONS,
                role=constants.RoleType.SUBSCRIBER,
                actions=constants.READ_ONLY_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.CLOSED_POSITION,
                group=constants.CollectionGroup.POSITIONS,
                role=constants.RoleType.SUBSCRIBER,
                actions=constants.READ_ONLY_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Order subscriber permissions
        items.append(
            self.create(
                collection=constants.CollectionName.FILLED_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.SUBSCRIBER,
                actions=constants.READ_ONLY_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.PARTIAL_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.SUBSCRIBER,
                actions=constants.READ_ONLY_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.PENDING_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.SUBSCRIBER,
                actions=constants.READ_ONLY_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.CANCELLED_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.SUBSCRIBER,
                actions=constants.READ_ONLY_ACTIONS,
                portfolio=portfolio,
            )
        )

        return items

    def default_guest_permissions(self, portfolio: AbstractPortfolio):
        items = []

        # Portfolio guest permissions
        items.append(
            self.create(
                collection=constants.CollectionName.PORTFOLIO,
                group=constants.CollectionGroup.PORTFOLIOS,
                role=constants.RoleType.GUEST,
                actions=constants.READ_ONLY_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Permission guest permissions
        items.append(
            self.create(
                collection=constants.CollectionName.PERMISSION,
                group=constants.CollectionGroup.PERMISSIONS,
                role=constants.RoleType.GUEST,
                actions=constants.READ_ONLY_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Subscription guest permissions
        items.append(
            self.create(
                collection=constants.CollectionName.SUBSCRIPTION,
                group=constants.CollectionGroup.SUBSCRIPTIONS,
                role=constants.RoleType.GUEST,
                actions=constants.NO_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Position guest permissions
        items.append(
            self.create(
                collection=constants.CollectionName.OPEN_POSITION,
                group=constants.CollectionGroup.POSITIONS,
                role=constants.RoleType.GUEST,
                actions=constants.NO_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.CLOSED_POSITION,
                group=constants.CollectionGroup.POSITIONS,
                role=constants.RoleType.GUEST,
                actions=constants.NO_ACTIONS,
                portfolio=portfolio,
            )
        )

        # Order guest permissions
        items.append(
            self.create(
                collection=constants.CollectionName.FILLED_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.GUEST,
                actions=constants.NO_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.PARTIAL_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.GUEST,
                actions=constants.NO_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.PENDING_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.GUEST,
                actions=constants.NO_ACTIONS,
                portfolio=portfolio,
            )
        )

        items.append(
            self.create(
                collection=constants.CollectionName.CANCELLED_ORDER,
                group=constants.CollectionGroup.ORDERS,
                role=constants.RoleType.GUEST,
                actions=constants.NO_ACTIONS,
                portfolio=portfolio,
            )
        )

        return items

    def get_queryset(self) -> PermissionQuerySet[AbstractPermissionType]:
        return PermissionQuerySet(model=self.model, using=self._db)


class PortfolioManager(models.Manager[AbstractPortfolioType]):

    def update_stats(self, portfolio: AbstractPortfolio) -> None:
        positions: PositionManager[AbstractPosition] = getattr(portfolio, "positions")
        qs = positions.get_queryset().closed_positions()
        profits = qs.calculate_profits()
        losses = qs.calculate_losses()
        washes = qs.calculate_washes()

        portfolio.avg_profit_amount = profits.get(qs.AMOUNT_AVG, 0)
        portfolio.smallest_profit_amount = profits.get(qs.AMOUNT_MIN, 0)
        portfolio.largest_profit_amount = profits.get(qs.AMOUNT_MAX, 0)

        portfolio.avg_loss_amount = losses.get(qs.AMOUNT_AVG, 0)
        portfolio.smallest_loss_amount = losses.get(qs.AMOUNT_MIN, 0)
        portfolio.largest_loss_amount = losses.get(qs.AMOUNT_MAX, 0)

        portfolio.avg_win_duration = profits.get(qs.DURATION_AVG, 0)
        portfolio.avg_loss_duration = losses.get(qs.DURATION_AVG, 0)
        portfolio.avg_wash_duration = washes.get(qs.DURATION_AVG, 0)

        portfolio.shortest_win_duration = profits.get(qs.DURATION_MIN, 0)
        portfolio.shortest_loss_duration = losses.get(qs.DURATION_MIN, 0)
        portfolio.shortest_wash_duration = washes.get(qs.DURATION_MIN, 0)

        portfolio.largest_win_duration = profits.get(qs.DURATION_MAX, 0)
        portfolio.largest_loss_duration = losses.get(qs.DURATION_MAX, 0)
        portfolio.largest_wash_duration = washes.get(qs.DURATION_MAX, 0)

        portfolio.total_wins = profits.get(qs.AMOUNT_CNT, 0)
        portfolio.total_losses = losses.get(qs.AMOUNT_CNT, 0)
        portfolio.total_washes = washes.get(qs.AMOUNT_CNT, 0)
        portfolio.total_trades = (
            portfolio.total_wins + portfolio.total_losses + portfolio.total_washes
        )

    def get_queryset(self) -> PortfolioQuerySet[AbstractPortfolioType]:
        return PortfolioQuerySet(model=self.model, using=self._db)


class SubscriptionManager(models.Manager[AbstractSubscriptionType]):

    def get_queryset(self) -> SubscriptionQuerySet[AbstractSubscriptionType]:
        return SubscriptionQuerySet(model=self.model, using=self._db)


class SymbolManager(models.Manager[AbstractSymbolType], ImportExportStub):

    insert_columns = [
        "code",
        "description",
        "exchange_id",
        "market_id",
        "security_id",
        "sic_id",
        "frontmonth",
        "naics_id",
        "search_index",
    ]

    def get_queryset(self) -> SymbolQuerySet[AbstractSymbolType]:
        return SymbolQuerySet(model=self.model, using=self._db)


class TempSymbolManager(models.Manager[AbstractTempSymbolType], ImportExportStub):

    import_columns = [
        "symbol",
        "description",
        "exchange",
        "listed_market",
        "security_type",
        "sic",
        "frontmonth",
        "naics",
    ]
    download_url = "https://www.iqfeed.net/downloads/download_file.cfm?type=mktsymbols"
    extract_folder = "/home/data/symbols"
    extract_file = "/mktsymbols_v2.txt"
    file_name = "/home/data/symbols/mktsymbols_v2.txt"

    def get_queryset(self) -> TempSymbolQuerySet[AbstractTempSymbolType]:
        return TempSymbolQuerySet(model=self.model, using=self._db)


class NaicsManager(models.Manager[AbstractNaicsCodeType], ImportExportStub):

    insert_columns = ["code"]
    import_columns = ["code", "description"]
    file_name = "/home/data/naics.tsv"

    def get_queryset(self) -> NaicsQuerySet[AbstractNaicsCodeType]:
        return NaicsQuerySet(model=self.model, using=self._db)


class SicManager(models.Manager[AbstractSicCodeType], ImportExportStub):

    insert_columns = ["code"]
    import_columns = ["code", "description"]
    file_name = "/home/data/sic.tsv"

    def get_queryset(self) -> SicQuerySet[AbstractSicCodeType]:
        return SicQuerySet(model=self.model, using=self._db)


class ExchangeManager(models.Manager[AbstractExchangeType], ImportExportStub):

    insert_columns = ["code"]
    import_columns = ["code", "description"]
    file_name = "/home/data/exchange.tsv"

    def get_queryset(self) -> ExchangeQuerySet[AbstractExchangeType]:
        return ExchangeQuerySet(model=self.model, using=self._db)


class MarketManager(models.Manager[AbstractMarketType], ImportExportStub):

    insert_columns = ["code"]
    import_columns = ["code", "description"]
    file_name = "/home/data/market.tsv"

    def get_queryset(self) -> MarketQuerySet[AbstractMarketType]:
        return MarketQuerySet(model=self.model, using=self._db)


class SecurityManager(models.Manager[AbstractSecurityType], ImportExportStub):

    insert_columns = ["code"]
    import_columns = ["code", "description"]
    file_name = "/home/data/security.tsv"

    def get_queryset(self) -> SecurityQuerySet[AbstractSecurityType]:
        return SecurityQuerySet(model=self.model, using=self._db)


class OrderManager(models.Manager[AbstractOrderType]):

    def get_queryset(self) -> OrderQuerySet[AbstractOrderType]:
        return OrderQuerySet(self.model, using=self._db)

    def update_status(self, order: AbstractOrder) -> None:
        if order.order_status == constants.OrderStatus.CANCELLED:
            pass
        elif order.filled_amount is None and order.sent_amount > 0:
            order.order_status = constants.OrderStatus.PENDING
        elif (order.filled_amount or 0) > 0 and (order.filled_amount or 0) < order.sent_amount:
            order.order_status = constants.OrderStatus.PARTIAL
        elif order.filled_amount == order.sent_amount:
            order.order_status = constants.OrderStatus.FILLED


# class GenericCTEManager(CTEManager, Generic[AbstractPositionType]):
#     pass
# CTEManager


class PositionManager(models.Manager[AbstractPositionType]):

    # def update_streaks(self) -> int:
    #     qs = self.get_queryset().closed_positions()
    #     index_subquery = qs.streak_index_query().filter(id=OuterRef("pk"))
    #     lag_subquery = qs.streak_lag_query().filter(id=OuterRef("pk"))
    #     sq = Subquery(index_subquery.values("group_index")[:1])
    #     update_response = qs.update(streak_index=sq)

    #     pprint.pprint(update_response)

    #     return qs.update(streak_group=Subquery(lag_subquery.values("group_id")[:1]))

    def update_status(self, position: AbstractPosition) -> None:
        orders: OrderManager[AbstractOrder] = getattr(position, "orders")
        rows = orders.get_queryset().order_stats()
        entry_order = rows[0] if len(rows) > 0 else {}
        exit_order = rows[1] if len(rows) > 1 else {}
        position.trend_type = constants.TrendType.UNKNOWN
        position.position_status = constants.PositionStatus.UNKNOWN
        position.duration = None
        position.real_pnl = None
        position.unreal_pnl = None

        # define entry for position
        if entry_order:
            position.entry_stamp = entry_order.get("first_order", 0)
            position.entry_price = entry_order.get("average_price", 0)
            position.entry_amount = entry_order.get("total_amount", 0)
            position.entry_fees = entry_order.get("total_fees", 0)
        else:
            # position.entry_stamp = None
            # position.entry_price = None
            # position.entry_amount = None
            position.entry_fees = None

        # define exit for position
        if exit_order:
            position.exit_stamp = exit_order.get("last_order", 0)
            position.exit_price = exit_order.get("avg_price", 0)
            position.exit_amount = exit_order.get("total_amount", 0)
            position.exit_fees = exit_order.get("total_fees", 0)
        else:
            position.exit_stamp = None
            position.exit_price = None
            position.exit_amount = None
            position.exit_fees = None

        # define the trend (long/short) for this position
        if entry_order.get("order_action", "") == constants.OrderAction.BUY:
            position.trend_type = constants.TrendType.LONG
        elif entry_order.get("order_action", "") == constants.OrderAction.SELL:
            position.trend_type = constants.TrendType.SHORT

        # define the position status
        if position.entry_amount == position.exit_amount and position.exit_amount is not None:
            position.position_status = constants.PositionStatus.CLOSED
        else:
            position.position_status = constants.PositionStatus.OPEN

        # calculate the amount of time the position was open
        current = datetime.datetime.now(position.entry_stamp.tzinfo)
        position.duration = (position.exit_stamp or current) - position.entry_stamp

        # calculate the amount of realized profit/loss for this position
        if position.exit_amount is not None:
            position.real_pnl = position.price_difference * (position.exit_amount or 0)
        # calculate the amount of unrealized profit/loss for this position
        if position.entry_price:
            position.unreal_pnl = position.entry_price * position.amount_difference

        # define the result type (win/loss/wash/none) for the position
        if position.position_status != constants.PositionStatus.CLOSED:
            position.result_type = constants.ResultType.UNKNOWN
        elif (position.real_pnl or 0) > 0:
            position.result_type = constants.ResultType.WIN
        elif (position.real_pnl or 0) < 0:
            position.result_type = constants.ResultType.LOSS
        elif position.real_pnl == 0:
            position.result_type = constants.ResultType.WASH

        position.save()

    def set_position(self, order: AbstractOrder) -> None:
        # Find the first open position for this portfolio and symbol
        portfolio_id: int | None = getattr(order.portfolio, "id", None)
        symbol_id: int | None = getattr(order.symbol, "id", None)

        if not portfolio_id or not symbol_id:
            return

        position = self.get_queryset().open_position_by(portfolio_id, symbol_id)

        # If a open position was not found then create a new one with the
        # current order as the extry order
        order.position = position if position else self.model()
        order.position.portfolio = order.portfolio
        order.position.symbol = order.symbol
        order.position.entry_stamp = order.sent_stamp
        order.position.entry_price = order.sent_price
        order.position.entry_amount = order.sent_amount
        order.position.save()

    def get_queryset(self) -> PositionQuerySet[AbstractPositionType]:
        return PositionQuerySet(model=self.model, using=self._db)
