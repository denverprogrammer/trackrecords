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
from django.db import models
from django.db.models import Q


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

    pending = Q(order_status=constants.OrderStatus.PENDING)

    partial = Q(order_status=constants.OrderStatus.PARTIAL)

    filled = Q(order_status=constants.OrderStatus.FILLED)

    cancelled = Q(order_status=constants.OrderStatus.CANCELLED)

    def pending_orders(self):
        return self.filter(self.pending)

    def partial_orders(self):
        return self.filter(self.partial)

    def filled_orders(self):
        return self.filter(self.filled)

    def cancelled_orders(self):
        return self.filter(self.cancelled)

    def executed_orders(self):
        return self.filter(self.filled | self.partial)

    def sort_pending(self):
        return self.pending_orders().order_by('sent_stamp')

    def sort_executed(self):
        return self.executed_orders().order_by('filled_stamp')


class PositionQuerySet(models.QuerySet[AbstractPosition]):

    def open_position_by(self, portfolio_id: int, symbol_id: int) -> AbstractPosition:
        return self.open_positions()\
            .positions_by_portfolio(portfolio_id)\
            .positions_by_symbol(symbol_id)\
            .first()

    def positions_by_portfolio(self, portfolio_id: int):
        return self.filter(portfolio__id=portfolio_id)

    def positions_by_symbol(self, symbol_id: int):
        return self.filter(symbol__id=symbol_id)

    def open_positions(self):
        return self.filter(position_status=constants.PositionStatus.OPEN)

    def closed_positions(self):
        return self.filter(position_status=constants.PositionStatus.CLOSED)
