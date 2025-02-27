from typing import Any, Dict, Generic, Self

from django.db import models
from django.db.models import (  # BigIntegerField,; Field,; IntegerField,; Window,
    Avg,
    Count,
    F,
    Max,
    Min,
    Q,
    StdDev,
    Sum,
)

# from django.db.models.expressions import Expression
# from django.db.models.functions import Cast, RowNumber
# from django_cte import CTEQuerySet, With
from vega import constants
from vega.models.Abstractions import (
    AbstractExchangeType,
    AbstractMarketType,
    AbstractNaicsCodeType,
    AbstractOrder,
    AbstractOrderType,
    AbstractPermissionType,
    AbstractPortfolioType,
    AbstractPosition,
    AbstractPositionType,
    AbstractSecurityType,
    AbstractSicCodeType,
    AbstractSubscriptionType,
    AbstractSymbolType,
    AbstractTempSymbolType,
)

# from vega.models.functions import CustomLag


class PermissionQuerySet(models.QuerySet[AbstractPermissionType], Generic[AbstractPermissionType]):
    pass


class PortfolioQuerySet(models.QuerySet[AbstractPortfolioType], Generic[AbstractPortfolioType]):
    pass


class SubscriptionQuerySet(
    models.QuerySet[AbstractSubscriptionType], Generic[AbstractSubscriptionType]
):
    pass


class SymbolQuerySet(models.QuerySet[AbstractSymbolType], Generic[AbstractSymbolType]):
    pass


class TempSymbolQuerySet(models.QuerySet[AbstractTempSymbolType], Generic[AbstractTempSymbolType]):

    def distinct_symbols(self):
        sql = """
            SELECT
                DISTINCT temp.symbol,
                temp.description,
                exchanges.id,
                markets.id,
                securities.id,
                COALESCE(sic_codes.id, NULL),
                temp.frontmonth,
                COALESCE(naics_codes.id, NULL),
                LEFT(CONCAT('(', exchanges.code, '):', temp.symbol, '  ', temp.description), 64)
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
        """

        return self.raw(sql.strip())

    def distinct_naics(self):
        return self.filter(naics__isnull=False).values("naics").distinct().order_by("naics")

    def distinct_sic(self):
        return self.filter(sic__isnull=False).values("sic").distinct().order_by("sic")

    def distinct_exchanges(self):
        return (
            self.filter(exchange__isnull=False).values("exchange").distinct().order_by("exchange")
        )

    def distinct_markets(self):
        return (
            self.filter(listed_market__isnull=False)
            .values("listed_market")
            .distinct()
            .order_by("listed_market")
        )

    def distinct_securities(self):
        return (
            self.filter(security_type__isnull=False)
            .values("security_type")
            .distinct()
            .order_by("security_type")
        )


class NaicsQuerySet(models.QuerySet[AbstractNaicsCodeType], Generic[AbstractNaicsCodeType]):
    pass


class SicQuerySet(models.QuerySet[AbstractSicCodeType], Generic[AbstractSicCodeType]):
    pass


class ExchangeQuerySet(models.QuerySet[AbstractExchangeType], Generic[AbstractExchangeType]):
    pass


class MarketQuerySet(models.QuerySet[AbstractMarketType], Generic[AbstractMarketType]):
    pass


class SecurityQuerySet(models.QuerySet[AbstractSecurityType], Generic[AbstractSecurityType]):
    pass


class OrderQuerySet(models.QuerySet[AbstractOrderType], Generic[AbstractOrderType]):

    IS_PENDING = Q(order_status=constants.OrderStatus.PENDING)

    IS_PARTIAL = Q(order_status=constants.OrderStatus.PARTIAL)

    IS_FILLED = Q(order_status=constants.OrderStatus.FILLED)

    IS_CANCELLED = Q(order_status=constants.OrderStatus.CANCELLED)

    ORDER_ACTION = F("order_action")

    FILLED_STAMP = F("filled_stamp")

    FILLED_AMOUNT = F("filled_amount")

    FILLED_PRICE = F("filled_price")

    FEES = F("fees")

    def order_stats(self) -> list[dict[str, Any]]:
        return list(
            self.filled_orders()
            .values("order_action")
            .annotate(order_count=Count(F("id")))
            .annotate(first_order=Min(self.FILLED_STAMP))
            .annotate(last_order=Max(self.FILLED_STAMP))
            .annotate(average_price=Avg(self.FILLED_PRICE))
            .annotate(total_amount=Sum(self.FILLED_AMOUNT))
            .annotate(total_fees=Sum(self.FEES))
            .order_by("filled_stamp")
        )

    def pending_orders(self) -> Self:
        return self.filter(self.IS_PENDING)

    def partial_orders(self) -> Self:
        return self.filter(self.IS_PARTIAL)

    def filled_orders(self) -> Self:
        return self.filter(self.IS_FILLED)

    def cancelled_orders(self) -> Self:
        return self.filter(self.IS_CANCELLED)

    def executed_orders(self) -> Self:
        return self.filter(self.IS_FILLED | self.IS_PARTIAL)

    def sort_pending(self) -> Self:
        return self.pending_orders().order_by(AbstractOrder.sent_stamp.column)

    def sort_executed(self) -> Self:
        return self.executed_orders().order_by(AbstractOrder.filled_stamp.column)


class PositionQuerySet(models.QuerySet[AbstractPositionType], Generic[AbstractPositionType]):

    RPNL_COL = F("real_pnl")

    UPNL_COL = F("unreal_pnl")

    DUR_COL = F("duration")

    EXIT_STAMP = F("exit_stamp")

    RESULT_TYPE = F("result_type")

    STREAK_INDEX = F("streak_index")

    PORTFOLIO_ID = F("portfolio_id")

    IS_PROFIT = Q(result_type=constants.ResultType.WIN)

    IS_LOSS = Q(result_type=constants.ResultType.LOSS)

    IS_WASH = Q(result_type=constants.ResultType.WASH)

    IS_UNKNOWN = Q(result_type=constants.ResultType.UNKNOWN)

    IS_OPEN = Q(position_status=constants.PositionStatus.OPEN)

    IS_CLOSED = Q(position_status=constants.PositionStatus.CLOSED)

    AMOUNT_AVG = "amount_avg"
    AMOUNT_MIN = "amount_min"
    AMOUNT_MAX = "amount_max"
    AMOUNT_CNT = "amount_cnt"

    DURATION_AVG = "duration_avg"
    DURATION_MIN = "duration_min"
    DURATION_MAX = "duration_max"

    # def streak_window(
    #     self, expression: Expression, output_field: Field[Any, Any] = IntegerField()
    # ) -> Window:
    #     return Window(
    #         expression=expression,
    #         order_by=[self.PORTFOLIO_ID.asc(), self.EXIT_STAMP.asc()],
    #         partition_by=[self.PORTFOLIO_ID, self.RESULT_TYPE],
    #         output_field=output_field,
    #     )

    # def streak_index_query(self) -> Self:
    #     offset_query = (
    #         self.all()
    #         .order_by(self.EXIT_STAMP)
    #         .closed_positions()
    #         .values("id")
    #         .annotate(offset=Cast(self.streak_window(RowNumber()) - 1, IntegerField()))
    #     )

    #     cte_offset = With(offset_query, name="cte_offset")
    #     joined_cte = cte_offset.join(self.all(), id=cte_offset.col.id)

    #     return (
    #         cast(Self, joined_cte)
    #         .with_cte(cte_offset)
    #         .values("id")
    #         .annotate(group_index=cte_offset.col.offset)
    #     )

    # def streak_lag_query(self) -> Self:
    #     lag_query = (
    #         self.all()
    #         .order_by(self.EXIT_STAMP)
    #         .closed_positions()
    #         .values("id")
    #         .annotate(
    #             lag_id=Cast(
    #                 self.streak_window(CustomLag(F("id"), self.STREAK_INDEX)), BigIntegerField()
    #             )
    #         )
    #     )

    #     cte_lag = With(lag_query, name="cte_lag")
    #     joined_cte = cte_lag.join(self.all(), id=cte_lag.col.id)

    #     return (
    #         cast(Self, joined_cte)
    #         .with_cte(cte_lag)
    #         .values("id")
    #         .annotate(group_id=cte_lag.col.lag_id)
    #     )

    def calculate_stats(self, column: F, query: Q) -> Dict[str, Any]:
        return self.aggregate(
            amount_avg=Avg(column, filter=query),
            amount_min=Min(column, filter=query),
            amount_max=Max(column, filter=query),
            amount_cnt=Count(column, filter=query),
            amount_stdev=StdDev(column, filter=query),
            amount_sum=Sum(column, filter=query),
            duration_avg=Avg(self.DUR_COL, filter=query),
            duration_min=Min(self.DUR_COL, filter=query),
            duration_max=Max(self.DUR_COL, filter=query),
            # duration_stdev=StdDev(self.DUR_COL, filter=query)
        )

    def calculate_profits(self) -> Dict[str, Any]:
        return self.calculate_stats(self.RPNL_COL, self.IS_PROFIT)

    def calculate_losses(self) -> Dict[str, Any]:
        return self.calculate_stats(self.RPNL_COL, self.IS_LOSS)

    def calculate_washes(self) -> Dict[str, Any]:
        return self.calculate_stats(self.RPNL_COL, self.IS_WASH)

    def open_position_by(self, portfolio_id: int, symbol_id: int) -> AbstractPosition | None:
        return (
            self.open_positions()
            .positions_by_portfolio(portfolio_id)
            .positions_by_symbol(symbol_id)
            .first()
        )

    def positions_by_portfolio(self, portfolio_id: int) -> Self:
        return self.filter(portfolio__id=portfolio_id)

    def positions_by_symbol(self, symbol_id: int) -> Self:
        return self.filter(symbol__id=symbol_id)

    def open_positions(self) -> Self:
        return self.filter(self.IS_OPEN)

    def closed_positions(self) -> Self:
        return self.filter(self.IS_CLOSED)
