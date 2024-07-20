from datetime import date, timedelta

from core import constants
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
from core.models.functions import CustomLag
from django.db import models
from django.db.models import (
    Avg,
    BigIntegerField,
    Case,
    Count,
    F,
    Field,
    IntegerField,
    Max,
    Min,
    Q,
    StdDev,
    Sum,
    Value,
    Variance,
    When,
    Window,
)
from django.db.models.expressions import Col, Expression, Func, RawSQL
from django.db.models.functions import Cast, Lag, RowNumber
from django_cte import CTEQuerySet, With


class PermissionQuerySet(models.QuerySet[AbstractPermission]):
    pass


class PortfolioQuerySet(models.QuerySet[AbstractPortfolio]):
    pass


class SubscriptionQuerySet(models.QuerySet[AbstractSubscription]):
    pass


class SymbolQuerySet(models.QuerySet[AbstractSymbol]):
    pass


class TempSymbolQuerySet(models.QuerySet[AbstractTempSymbol]):

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


class NaicsQuerySet(models.QuerySet[AbstractNaicsCode]):
    pass


class SicQuerySet(models.QuerySet[AbstractSicCode]):
    pass


class ExchangeQuerySet(models.QuerySet[AbstractExchange]):
    pass


class MarketQuerySet(models.QuerySet[AbstractMarket]):
    pass


class SecurityQuerySet(models.QuerySet[AbstractSecurity]):
    pass


class OrderQuerySet(models.QuerySet[AbstractOrder]):

    ISPENDING = Q(order_status=constants.OrderStatus.PENDING)

    ISPARTIAL = Q(order_status=constants.OrderStatus.PARTIAL)

    IS_FILLED = Q(order_status=constants.OrderStatus.FILLED)

    IS_CANCELLED = Q(order_status=constants.OrderStatus.CANCELLED)

    ORDER_ACTION = F('order_action')

    FILLED_STAMP = F('filled_stamp')

    FILLED_AMOUNT = F('filled_amount')

    FILLED_PRICE = F('filled_price')

    FEES = F('fees')

    def order_stats(self) -> 'OrderQuerySet':
        return self.filled_orders()\
            .values('order_action')\
            .annotate(order_count=Count(F('id')))\
            .annotate(first_order=Min(self.FILLED_STAMP))\
            .annotate(last_order=Max(self.FILLED_STAMP))\
            .annotate(average_price=Avg(self.FILLED_PRICE))\
            .annotate(total_amount=Sum(self.FILLED_AMOUNT))\
            .annotate(total_fees=Sum(self.FEES))\
            .order_by('filled_stamp')

    def pending_orders(self):
        return self.filter(self.PENDING)

    def partial_orders(self):
        return self.filter(self.PARTIAL)

    def filled_orders(self):
        return self.filter(self.IS_FILLED)

    def cancelled_orders(self):
        return self.filter(self.IS_CANCELLED)

    def executed_orders(self):
        return self.filter(self.IS_FILLED | self.PARTIAL)

    def sort_pending(self):
        return self.pending_orders().order_by(AbstractOrder.sent_stamp.column)

    def sort_executed(self):
        return self.executed_orders().order_by(AbstractOrder.filled_stamp.column)


class PositionQuerySet(CTEQuerySet[AbstractPosition]):

    RPNL_COL = F('real_pnl')

    UPNL_COL = F('unreal_pnl')

    DUR_COL = F('duration')

    EXIT_STAMP = F('exit_stamp')

    RESULT_TYPE = F('result_type')

    STREAK_INDEX = F('streak_index')

    PORTFOLIO_ID = F('portfolio_id')

    IS_PROFIT = Q(result_type=constants.ResultType.WIN)

    IS_LOSS = Q(result_type=constants.ResultType.LOSS)

    IS_WASH = Q(result_type=constants.ResultType.WASH)

    IS_UNKNOWN = Q(result_type=constants.ResultType.UNKNOWN)

    IS_OPEN = Q(position_status=constants.PositionStatus.OPEN)

    IS_CLOSED = Q(position_status=constants.PositionStatus.CLOSED)

    AMOUNT_AVG = 'amount_avg'
    AMOUNT_MIN = 'amount_min'
    AMOUNT_MAX = 'amount_max'
    AMOUNT_CNT = 'amount_cnt'

    DURATION_AVG = 'duration_avg'
    DURATION_MIN = 'duration_min'
    DURATION_MAX = 'duration_max'

    def streak_window(self, expression: Expression, output_field: Field = IntegerField()) -> Window:
        return Window(
            expression=expression,
            order_by=[self.PORTFOLIO_ID.asc(), self.EXIT_STAMP.asc()],
            partition_by=[self.PORTFOLIO_ID, self.RESULT_TYPE],
            output_field=output_field
        )

    def streak_index_query(self) -> 'PositionQuerySet':
        offset_query = self.all().order_by(self.EXIT_STAMP)\
            .closed_positions()\
            .values('id')\
            .annotate(offset=Cast(
                self.streak_window(RowNumber()) - 1,
                IntegerField()
            )
        )

        cte_offset = With(offset_query, name='cte_offset')

        return (
            cte_offset.join(self.all(), id=cte_offset.col.id)
            .with_cte(cte_offset)
            .values('id')
            .annotate(group_index=cte_offset.col.offset)
        )

    def streak_lag_query(self) -> 'PositionQuerySet':
        lag_query = self.all().order_by(self.EXIT_STAMP)\
            .closed_positions()\
            .values('id')\
            .annotate(lag_id=Cast(
                self.streak_window(CustomLag(F('id'), self.STREAK_INDEX)),
                BigIntegerField()
            )
        )

        cte_lag = With(lag_query, name='cte_lag')

        return (
            cte_lag.join(self.all(), id=cte_lag.col.id)
            .with_cte(cte_lag)
            .values('id')
            .annotate(group_id=cte_lag.col.lag_id)
        )

    def calculate_stats(self, column: F, query: filter):
        return self.aggregate(
            amount_avg=Avg(column, filter=query),
            amount_min=Min(column, filter=query),
            amount_max=Max(column, filter=query),
            amount_cnt=Count(column, filter=query),
            amount_stdev=StdDev(column, filter=query),
            amount_sum=Sum(column, filter=query),
            duration_avg=Avg(self.DUR_COL, filter=query),
            duration_min=Min(self.DUR_COL, filter=query),
            duration_max=Max(self.DUR_COL, filter=query)
            # duration_stdev=StdDev(self.DUR_COL, filter=query)
        )

    def calculate_profits(self) -> 'PositionQuerySet':
        return self.calculate_stats(self.RPNL_COL, self.IS_PROFIT)

    def calculate_losses(self) -> 'PositionQuerySet':
        return self.calculate_stats(self.RPNL_COL, self.IS_LOSS)

    def calculate_washes(self) -> 'PositionQuerySet':
        return self.calculate_stats(self.RPNL_COL, self.IS_WASH)

    def open_position_by(self, portfolio_id: int, symbol_id: int) -> AbstractPosition:
        return self.open_positions()\
            .positions_by_portfolio(portfolio_id)\
            .positions_by_symbol(symbol_id)\
            .first()

    def positions_by_portfolio(self, portfolio_id: int) -> 'PositionQuerySet':
        return self.filter(portfolio__id=portfolio_id)

    def positions_by_symbol(self, symbol_id: int) -> 'PositionQuerySet':
        return self.filter(symbol__id=symbol_id)

    def open_positions(self) -> 'PositionQuerySet':
        return self.filter(self.IS_OPEN)

    def closed_positions(self) -> 'PositionQuerySet':
        return self.filter(self.IS_CLOSED)
