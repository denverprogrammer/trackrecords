from core import constants
from core.constants import AppNames
from core.forms import ChoiceArrayField
from core.models._ModelStubs import CodeStub
from django.db import models


class _NaicsCode(CodeStub):

    class Meta(CodeStub.Meta):
        app_label = AppNames.DATASET
        abstract = True


class _SicCode(CodeStub):

    class Meta(CodeStub.Meta):
        app_label = AppNames.DATASET
        abstract = True


class _Exchange(CodeStub):

    class Meta(CodeStub.Meta):
        app_label = AppNames.DATASET
        abstract = True


class _Market(CodeStub):

    class Meta(CodeStub.Meta):
        app_label = AppNames.DATASET
        abstract = True


class _Security(CodeStub):

    class Meta(CodeStub.Meta):
        app_label = AppNames.DATASET
        abstract = True
        verbose_name_plural = 'securities'


class _Symbol(CodeStub):

    frontmonth = models.CharField(max_length=1, null=True, blank=True)

    class Meta(CodeStub.Meta):
        app_label = AppNames.DATASET
        abstract = True
        ordering = ['exchange__code', 'code']

    def __str__(self):
        return f'({self.exchange.code}):{self.code}'


class _TempSymbol(models.Model):

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


class _Portfolio(CodeStub):

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


class _Position(models.Model):

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

    class Meta:
        app_label = AppNames.TRACKRECORD
        abstract = True

    def __str__(self):
        return self.portfolio.code


class _Order(models.Model):

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

    class Meta:
        app_label = AppNames.TRACKRECORD
        abstract = True

    def __str__(self):
        return self.symbol.code


class _Permission(models.Model):

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


class _Subscription(models.Model):

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
