import typing
from typing import Iterable, Optional

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
from django.conf import settings
from django.db import models


class NaicsCode(AbstractNaicsCode):

    objects: NaicsManager = NaicsManager()


class SicCode(AbstractSicCode):

    objects: SicManager = SicManager()


class Exchange(AbstractExchange):

    objects: ExchangeManager = ExchangeManager()


class Market(AbstractMarket):

    objects: MarketManager = MarketManager()


class Security(AbstractSecurity):

    objects: SecurityManager = SecurityManager()


class Symbol(AbstractSymbol):

    exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name=constants.ModelClass.EXCHANGE
    )

    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name=constants.ModelClass.MARKET
    )

    security = models.ForeignKey(
        Security,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name=constants.ModelClass.SECURITY
    )

    sic = models.ForeignKey(
        SicCode,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name=constants.ModelClass.SIC_CODE
    )

    naics = models.ForeignKey(
        NaicsCode,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name=constants.ModelClass.NAICS_CODE
    )

    objects: SymbolManager = SymbolManager()


class TempSymbol(AbstractTempSymbol):

    objects: TempSymbolManager = TempSymbolManager()


class Portfolio(AbstractPortfolio):

    objects: PortfolioManager = PortfolioManager()


class Position(AbstractPosition):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.POSITIONS,
        related_query_name=constants.ModelClass.PORTFOLIO
    )

    symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name=constants.CollectionGroup.POSITIONS,
        related_query_name=constants.ModelClass.SYMBOL
    )

    objects: PositionManager = PositionManager()


class Order(AbstractOrder):

    position = models.ForeignKey(
        Position,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.ORDERS,
        related_query_name=constants.ModelClass.POSITION
    )

    symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.ORDERS,
        related_query_name=constants.ModelClass.SYMBOL
    )

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.ORDERS,
        related_query_name=constants.ModelClass.PORTFOLIO
    )

    objects: OrderManager = OrderManager()


class Permission(AbstractPermission):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.PERMISSIONS,
        related_query_name=constants.ModelClass.PORTFOLIO
    )

    objects: PermissionManager = PermissionManager()


class Subscription(AbstractSubscription):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SUBSCRIPTIONS,
        related_query_name=constants.ModelClass.PORTFOLIO
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SUBSCRIPTIONS,
        related_query_name='auth.user'
    )

    objects: SubscriptionManager = SubscriptionManager()
