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
        related_name=constants.CollectionGroup.SYMBOLS
    )

    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SYMBOLS
    )

    security = models.ForeignKey(
        Security,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SYMBOLS
    )

    sic = models.ForeignKey(
        SicCode,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name=constants.CollectionGroup.SYMBOLS
    )

    naics = models.ForeignKey(
        NaicsCode,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name=constants.CollectionGroup.SYMBOLS
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
        related_name=constants.CollectionGroup.POSITIONS
    )

    symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name=constants.CollectionGroup.POSITIONS
    )

    objects: PositionManager = PositionManager()


class Order(_Order):

    symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.ORDERS
    )

    position = models.ForeignKey(
        Position,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.ORDERS
    )

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.ORDERS
    )

    objects: OrderManager = OrderManager()


class Permission(_Permission):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.PERMISSIONS
    )

    objects: PermissionManager = PermissionManager()


class Subscription(_Subscription):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SUBSCRIPTIONS
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SUBSCRIPTIONS
    )

    objects: SubscriptionManager = SubscriptionManager()
