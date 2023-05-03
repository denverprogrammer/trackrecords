from core import constants
from core.models._managers import (
    ExchangeManager,
    MarketManager,
    NaicsManager,
    OrderManager,
    PermissionManager,
    PortfolioManager,
    PositionManager,
    SecurityManager,
    SicManager,
    SubscriptionManager,
    SymbolManager,
    TempSymbolManager,
)
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


class NaicsCode(_NaicsCode):

    objects: NaicsManager = NaicsManager()


class SicCode(_SicCode):

    objects: SicManager = SicManager()


class Exchange(_Exchange):

    objects: ExchangeManager = ExchangeManager()


class Market(_Market):

    objects: MarketManager = MarketManager()


class Security(_Security):

    objects: SecurityManager = SecurityManager()


class Symbol(_Symbol):

    exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name='core.exchange'
    )

    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name='core.market'
    )

    security = models.ForeignKey(
        Security,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name='core.security'
    )

    sic = models.ForeignKey(
        SicCode,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name='core.siccode'
    )

    naics = models.ForeignKey(
        NaicsCode,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name='core.naicscode'
    )

    objects: SymbolManager = SymbolManager()


class TempSymbol(_TempSymbol):

    objects: TempSymbolManager = TempSymbolManager()


class Portfolio(_Portfolio):

    objects: PortfolioManager = PortfolioManager()


class Position(_Position):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.POSITIONS,
        related_query_name='core.portfolio'
    )

    symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name=constants.CollectionGroup.POSITIONS,
        related_query_name='core.symbol'
    )

    objects: PositionManager = PositionManager()


class Order(_Order):

    position = models.ForeignKey(
        Position,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.ORDERS,
        related_query_name='core.position'
    )

    symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.ORDERS,
        related_query_name='core.symbol'
    )

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.ORDERS,
        related_query_name='core.portfolio'
    )

    objects: OrderManager = OrderManager()


class Permission(_Permission):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.PERMISSIONS,
        related_query_name='core.portfolio'
    )

    objects: PermissionManager = PermissionManager()


class Subscription(_Subscription):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SUBSCRIPTIONS,
        related_query_name='core.portfolio'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SUBSCRIPTIONS,
        related_query_name='auth.user'
    )

    objects: SubscriptionManager = SubscriptionManager()
