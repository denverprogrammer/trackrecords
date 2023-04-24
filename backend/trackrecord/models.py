# Create your models here.
from core import constants
from core.forms import ChoiceArrayField
from dataset.models import Symbol
from django.db import models


class Portfolio(models.Model):
    code = models.CharField(max_length=32, db_index=True)

    description = models.CharField(max_length=64)

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

    avg_profit = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    avg_duration = models.DurationField(null=True)

    win_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    total_cagr = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return self.code


class Position(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

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

    def __str__(self):
        return self.portfolio.code


class Order(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)

    position = models.ForeignKey(
        Position,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

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
        max_digits=9, decimal_places=2, null=True, blank=True)

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

    def __str__(self):
        return self.symbol.code


class Permission(models.Model):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='permissions'
    )

    collection = models.CharField(
        max_length=15,
        choices=constants.CollectionType.choices,
        default=constants.CollectionType.PORTFOLIO,
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

    class Meta:
        ordering = ['collection', 'role']

    def __str__(self):
        return "%s %s" % (self.collection, self.role)
