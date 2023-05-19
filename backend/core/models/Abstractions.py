from core import constants
from core.constants import AppNames
from core.forms import ChoiceArrayField
from core.models._ModelStubs import CodeStub
from django.db import models


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

    frontmonth = models.CharField(max_length=1, null=True, blank=True)

    class Meta(CodeStub.Meta):
        app_label = AppNames.DATASET
        abstract = True
        ordering = ['exchange__code', 'code']

    def __str__(self):
        return f'({self.exchange.code}):{self.code}'


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


class AbstractPortfolio(CodeStub):

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

    avg_profit = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    avg_duration = models.DurationField(null=True)

    win_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    total_cagr = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta(CodeStub.Meta):
        app_label = AppNames.TRACKRECORD
        abstract = True


class AbstractPosition(models.Model):

    trend_type = models.CharField(
        max_length=5,
        choices=constants.TrendType.choices,
        default=constants.TrendType.LONG,
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

    class Meta:
        app_label = AppNames.TRACKRECORD
        abstract = True
        ordering = ['exit_stamp', 'entry_stamp']

    def __str__(self):
        return self.portfolio.code


class AbstractOrder(models.Model):

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


class AbstractPermission(models.Model):

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


class AbstractSubscription(models.Model):

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
