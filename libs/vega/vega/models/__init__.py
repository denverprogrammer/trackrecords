from typing import Optional, Self, cast

from django.conf import settings
from django.db import models
from vega import constants
from vega.models._managers import (
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
from vega.models.Abstractions import (
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


class NaicsCode(AbstractNaicsCode):

    symbols: models.Manager["Symbol"]

    objects = cast(NaicsManager[Self], NaicsManager())


class SicCode(AbstractSicCode):

    symbols: models.Manager["Symbol"]

    objects = cast(SicManager[Self], SicManager())


class Exchange(AbstractExchange):

    symbols: models.Manager["Symbol"]

    objects = cast(ExchangeManager[Self], ExchangeManager())


class Market(AbstractMarket):

    symbols: models.Manager["Symbol"]

    objects = cast(MarketManager[Self], MarketManager())


class Security(AbstractSecurity):

    symbols: models.Manager["Symbol"]

    objects = cast(SecurityManager[Self], SecurityManager())


class Symbol(AbstractSymbol):

    exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name=constants.ModelClass.EXCHANGE,
    )

    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name=constants.ModelClass.MARKET,
    )

    security = models.ForeignKey(
        Security,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name=constants.ModelClass.SECURITY,
    )

    sic = models.ForeignKey(
        SicCode,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name=constants.ModelClass.SIC_CODE,
    )

    naics = models.ForeignKey(
        NaicsCode,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name=constants.CollectionGroup.SYMBOLS,
        related_query_name=constants.ModelClass.NAICS_CODE,
    )

    orders: models.Manager["Order"]

    positions: models.Manager["Position"]

    objects = cast(SymbolManager[Self], SymbolManager())


class TempSymbol(AbstractTempSymbol):

    objects = cast(TempSymbolManager[Self], TempSymbolManager())


class Portfolio(AbstractPortfolio):

    orders: models.Manager["Order"]

    positions: models.Manager["Position"]

    permissions: models.Manager["Permission"]

    subscriptions: models.Manager["Subscription"]

    objects = cast(PortfolioManager[Self], PortfolioManager())


class Position(AbstractPosition):

    _portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.POSITIONS,
        related_query_name=constants.ModelClass.PORTFOLIO,
    )

    _symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name=constants.CollectionGroup.POSITIONS,
        related_query_name=constants.ModelClass.SYMBOL,
    )

    objects = cast(PositionManager[Self], PositionManager())

    orders: OrderManager["AbstractOrder"]

    @property
    def symbol(self) -> Optional[AbstractSymbol]:
        return self._symbol

    @symbol.setter
    def symbol(self, value: Optional[AbstractSymbol]) -> Self:
        self._symbol = value

        return self

    @property
    def portfolio(self) -> AbstractPortfolio:
        return self._portfolio

    @portfolio.setter
    def portfolio(self, value: AbstractPortfolio) -> Self:
        self._portfolio = value

        return self


class Order(AbstractOrder):

    _position = models.ForeignKey(
        Position,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.ORDERS,
        related_query_name=constants.ModelClass.POSITION,
    )

    _symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.ORDERS,
        related_query_name=constants.ModelClass.SYMBOL,
    )

    _portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.ORDERS,
        related_query_name=constants.ModelClass.PORTFOLIO,
    )

    objects = cast(OrderManager[Self], OrderManager())

    @property
    def position(self) -> Optional[AbstractPosition]:
        return self._position

    @position.setter
    def position(self, value: Optional[AbstractPosition]) -> Self:
        self._position = value

        return self

    @property
    def symbol(self) -> AbstractSymbol:
        return self._symbol

    @symbol.setter
    def symbol(self, value: AbstractSymbol) -> Self:
        self._symbol = value

        return self

    @property
    def portfolio(self) -> AbstractPortfolio:
        return self._portfolio

    @portfolio.setter
    def portfolio(self, value: AbstractPortfolio) -> Self:
        self._portfolio = value

        return self


class Permission(AbstractPermission):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.PERMISSIONS,
        related_query_name=constants.ModelClass.PORTFOLIO,
    )

    objects = cast(PermissionManager[Self], PermissionManager())


class Subscription(AbstractSubscription):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SUBSCRIPTIONS,
        related_query_name=constants.ModelClass.PORTFOLIO,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name=constants.CollectionGroup.SUBSCRIPTIONS,
        related_query_name="auth.user",
    )

    objects = cast(SubscriptionManager[Self], SubscriptionManager())
