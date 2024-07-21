from decimal import Decimal

from django.db import models
from vega import constants
from vega.constants import AppNames
from vega.forms import ChoiceArrayField
from vega.models._ModelStubs import CodeStub, EventBridgeStub


class AbstractNaicsCode(CodeStub):

    class Meta(CodeStub.Meta):
        app_label = AppNames.DATASET
        abstract = True


class AbstractSicCode(CodeStub):

    class Meta(CodeStub.Meta):
        app_label = AppNames.DATASET
        abstract = True


class AbstractExchange(CodeStub):

    class Meta(CodeStub.Meta):
        app_label = AppNames.DATASET
        abstract = True


class AbstractMarket(CodeStub):

    class Meta(CodeStub.Meta):
        app_label = AppNames.DATASET
        abstract = True


class AbstractSecurity(CodeStub):

    class Meta(CodeStub.Meta):
        app_label = AppNames.DATASET
        abstract = True
        verbose_name_plural = 'securities'


class AbstractSymbol(CodeStub):

    search_index = models.CharField(max_length=64, unique=True)

    frontmonth = models.CharField(max_length=1, null=True, blank=True)

    class Meta(CodeStub.Meta):
        app_label = AppNames.DATASET
        abstract = True
        ordering = ['search_index']

    def __str__(self):
        return self.search_index

    def save(self, *args, **kwargs):
        text = f'({self.exchange.code}):{self.code} {self.description}'
        self.search_index = text[64:]
        super(AbstractSymbol, self).save(*args, **kwargs)


class AbstractTempSymbol(models.Model):

    symbol = models.CharField(max_length=32, null=True, blank=True)

    description = models.CharField(max_length=150, null=True, blank=True)

    exchange = models.CharField(max_length=16, null=True, blank=True)

    listed_market = models.CharField(max_length=16, null=True, blank=True)

    security_type = models.CharField(max_length=16, null=True, blank=True)

    sic = models.CharField(max_length=8, null=True, blank=True)

    frontmonth = models.CharField(max_length=1, null=True, blank=True)

    naics = models.CharField(max_length=16, null=True, blank=True)

    class Meta:
        app_label = AppNames.DATASET
        abstract = True
        ordering = ['symbol']

    def __str__(self):
        return f'({self.exchange.code}):{self.symbol.code}'


class AbstractPortfolio(CodeStub, EventBridgeStub):

    initial_capital = models.DecimalField(max_digits=9, decimal_places=2)

    record_type = models.CharField(
        max_length=8,
        choices=constants.RecordType.choices,
        default=constants.RecordType.ORDER,
    )

    entry_type = models.CharField(
        max_length=10,
        choices=constants.EntryType.choices,
        default=constants.EntryType.MANUAL,
    )

    allowed_roles = ChoiceArrayField(
        models.CharField(
            max_length=10,
            choices=constants.RoleType.choices,
            default=constants.RoleType.OWNER
        )
    )

    avg_profit_amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )

    smallest_profit_amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )

    largest_profit_amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )

    avg_loss_amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )

    smallest_loss_amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )

    largest_loss_amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )

    avg_win_duration = models.DurationField(null=True, blank=True)

    avg_loss_duration = models.DurationField(null=True, blank=True)

    avg_wash_duration = models.DurationField(null=True, blank=True)

    shortest_win_duration = models.DurationField(null=True, blank=True)

    shortest_loss_duration = models.DurationField(null=True, blank=True)

    shortest_wash_duration = models.DurationField(null=True, blank=True)

    largest_win_duration = models.DurationField(null=True, blank=True)

    largest_loss_duration = models.DurationField(null=True, blank=True)

    largest_wash_duration = models.DurationField(null=True, blank=True)

    win_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    total_cagr = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    total_wins = models.IntegerField(null=True, blank=True)

    total_losses = models.IntegerField(null=True, blank=True)

    total_washes = models.IntegerField(null=True, blank=True)

    total_trades = models.IntegerField(null=True, blank=True)

    open_trades = models.IntegerField(null=True, blank=True)

    largest_wining_streak = models.IntegerField(null=True, blank=True)

    largest_loosing_streak = models.IntegerField(null=True, blank=True)

    largest_wash_streak = models.IntegerField(null=True, blank=True)

    class Meta(CodeStub.Meta):
        app_label = AppNames.TRACKRECORD
        abstract = True


class AbstractPosition(models.Model, EventBridgeStub):

    trend_type = models.CharField(
        max_length=7,
        choices=constants.TrendType.choices,
        default=constants.TrendType.UNKNOWN,
    )

    position_status = models.CharField(
        max_length=6,
        choices=constants.PositionStatus.choices,
        default=constants.PositionStatus.OPEN,
    )

    entry_stamp = models.DateTimeField(auto_now=False, auto_now_add=False)

    entry_price = models.DecimalField(max_digits=9, decimal_places=2)

    entry_amount = models.IntegerField()

    entry_fees = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )

    exit_stamp = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )

    exit_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        blank=True,
        null=True
    )

    exit_amount = models.IntegerField(blank=True, null=True)

    exit_fees = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )

    real_pnl = models.DecimalField(
        blank=True,
        null=True,
        max_digits=9,
        decimal_places=2
    )

    unreal_pnl = models.DecimalField(
        blank=True,
        null=True,
        max_digits=9,
        decimal_places=2
    )

    duration = models.DurationField(null=True, blank=True)

    result_type = models.CharField(
        max_length=7,
        choices=constants.ResultType.choices,
        null=True,
        blank=True
    )

    streak_group = models.BigIntegerField(blank=True, null=True)

    streak_index = models.PositiveIntegerField(blank=True, null=True)

    @property
    def price_difference(self) -> Decimal:
        if self.exit_price and self.entry_price:
            return self.exit_price - self.entry_price
        return 0

    @property
    def amount_difference(self) -> int:
        if self.entry_amount and self.exit_amount:
            return self.entry_amount - self.exit_amount
        elif self.entry_amount and self.exit_amount is None:
            return self.entry_amount
        return 0

    class Meta:
        app_label = AppNames.TRACKRECORD
        abstract = True
        ordering = ['exit_stamp', 'entry_stamp']

    def __str__(self):
        return self.portfolio.code


class AbstractOrder(models.Model, EventBridgeStub):

    order_type = models.CharField(
        max_length=10,
        choices=constants.OrderType.choices,
        default=constants.OrderType.MARKET,
    )

    order_action = models.CharField(
        max_length=4,
        choices=constants.OrderAction.choices,
        default=constants.OrderAction.BUY,
    )

    order_status = models.CharField(
        max_length=10,
        choices=constants.OrderStatus.choices,
        default=constants.OrderStatus.PENDING,
    )

    sent_stamp = models.DateTimeField(auto_now=False, auto_now_add=False)

    sent_price = models.DecimalField(max_digits=9, decimal_places=2)

    limit_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )

    sent_amount = models.IntegerField()

    filled_stamp = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True
    )

    filled_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )

    filled_amount = models.IntegerField(null=True, blank=True)

    fees = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        app_label = AppNames.TRACKRECORD
        abstract = True
        ordering = ['filled_stamp', 'sent_stamp']

    def __str__(self):
        return self.symbol.code

    def hasAmount(self) -> bool:
        return self.order_status in [
            constants.OrderStatus.FILLED,
            constants.OrderStatus.PARTIAL
        ]


class AbstractPermission(models.Model, EventBridgeStub):

    collection = models.CharField(
        max_length=15,
        choices=constants.CollectionName.choices,
        default=constants.CollectionName.PORTFOLIO,
    )

    group = models.CharField(
        max_length=15,
        choices=constants.CollectionGroup.choices,
        default=constants.CollectionGroup.PORTFOLIOS,
    )

    role = models.CharField(
        max_length=10,
        choices=constants.RoleType.choices,
        default=constants.RoleType.SUBSCRIBER,
    )

    actions = ChoiceArrayField(
        models.CharField(
            max_length=6,
            choices=constants.ActionType.choices,
            default=constants.ActionType.VIEW
        )
    )

    enabled = models.BooleanField(default=False)

    class Meta:
        app_label = AppNames.TRACKRECORD
        abstract = True
        ordering = ['role', 'group', 'collection']

    def __str__(self):
        return "%s %s" % (self.role, self.collection)


class AbstractSubscription(models.Model, EventBridgeStub):

    role = models.CharField(
        max_length=10,
        choices=constants.RoleType.choices,
        default=constants.RoleType.OWNER,
    )

    class Meta:
        app_label = AppNames.TRACKRECORD
        abstract = True

    def __str__(self):
        return "%s %s" % (self.user.username, self.portfolio.code)
