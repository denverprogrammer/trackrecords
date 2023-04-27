# Create your models here.
import typing

from core import constants
from core.forms import ChoiceArrayField
from dataset.models import Symbol
from django.conf import settings
from django.db import models


class PermissionQuerySet(models.QuerySet['Permission']):
    pass


class PortfolioQuerySet(models.QuerySet['Portfolio']):
    pass


class SubscriptionQuerySet(models.QuerySet['Subscription']):
    pass


class PermissionManager(models.Manager['Permission']):
    _CREATE = constants.ActionType.CREATE
    _UPDATE = constants.ActionType.UPDATE
    _VIEW = constants.ActionType.VIEW
    _LIST = constants.ActionType.LIST
    _DELETE = constants.ActionType.DELETE

    _NO_ACTIONS = []
    _ALL_ACTIONS = [_CREATE, _UPDATE, _VIEW, _LIST, _DELETE]
    _READ_ONLY_ACTIONS = [_VIEW, _LIST]
    _NO_CREATE_ACTIONS = [_UPDATE, _VIEW, _LIST, _DELETE]
    _NO_DELETE_ACTIONS = [_CREATE, _UPDATE, _VIEW, _LIST]
    _NO_CREATE_OR_DELETE_ACTIONS = [_UPDATE, _VIEW, _LIST]

    def default_permissions(self, portfolio):
        items = []

        #########################
        ##  Owner Permissions  ##
        #########################

        # Portfolio owner permissions
        items.append(Permission(
            collection=constants.CollectionName.PORTFOLIO,
            group=constants.CollectionGroup.PORTFOLIO,
            role=constants.RoleType.OWNER,
            actions=self._NO_CREATE_ACTIONS,
            portfolio=portfolio
        ))

        # Permission owner permissions
        items.append(Permission(
            collection=constants.CollectionName.PERMISSION,
            group=constants.CollectionGroup.PERMISSION,
            role=constants.RoleType.OWNER,
            actions=self._NO_CREATE_OR_DELETE_ACTIONS,
            portfolio=portfolio
        ))

        # Subscription owner permissions
        items.append(Permission(
            collection=constants.CollectionName.SUBSCRIPTION,
            group=constants.CollectionGroup.SUBSCRIPTION,
            role=constants.RoleType.OWNER,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        # Position owner permissions
        items.append(Permission(
            collection=constants.CollectionName.OPEN_POSITION,
            group=constants.CollectionGroup.POSITION,
            role=constants.RoleType.OWNER,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.CLOSED_POSITION,
            group=constants.CollectionGroup.POSITION,
            role=constants.RoleType.OWNER,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        # Order order permissions
        items.append(Permission(
            collection=constants.CollectionName.FILLED_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.OWNER,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.PARTIAL_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.OWNER,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.PENDING_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.OWNER,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.CANCELLED_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.OWNER,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        #########################
        ##  Admin Permissions  ##
        #########################

        # Portfolio admin permissions
        items.append(Permission(
            collection=constants.CollectionName.PORTFOLIO,
            group=constants.CollectionGroup.PORTFOLIO,
            role=constants.RoleType.ADMIN,
            actions=self._NO_CREATE_OR_DELETE_ACTIONS,
            portfolio=portfolio
        ))

        # Permission admin permissions
        items.append(Permission(
            collection=constants.CollectionName.PERMISSION,
            group=constants.CollectionGroup.PERMISSION,
            role=constants.RoleType.ADMIN,
            actions=self._NO_CREATE_OR_DELETE_ACTIONS,
            portfolio=portfolio
        ))

        # Subscription admin permissions
        items.append(Permission(
            collection=constants.CollectionName.SUBSCRIPTION,
            group=constants.CollectionGroup.SUBSCRIPTION,
            role=constants.RoleType.ADMIN,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        # Position admin permissions
        items.append(Permission(
            collection=constants.CollectionName.OPEN_POSITION,
            group=constants.CollectionGroup.POSITION,
            role=constants.RoleType.ADMIN,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.CLOSED_POSITION,
            group=constants.CollectionGroup.POSITION,
            role=constants.RoleType.ADMIN,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        # Order admin permissions
        items.append(Permission(
            collection=constants.CollectionName.FILLED_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.ADMIN,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.PARTIAL_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.ADMIN,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.PENDING_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.ADMIN,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.CANCELLED_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.ADMIN,
            actions=self._ALL_ACTIONS,
            portfolio=portfolio
        ))

        ##############################
        ##  Subscriber Permissions  ##
        ##############################

        # Portfolio subscriber permissions
        items.append(Permission(
            collection=constants.CollectionName.PORTFOLIO,
            group=constants.CollectionGroup.PORTFOLIO,
            role=constants.RoleType.SUBSCRIBER,
            actions=self._READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        # Permission subscriber permissions
        items.append(Permission(
            collection=constants.CollectionName.PERMISSION,
            group=constants.CollectionGroup.PERMISSION,
            role=constants.RoleType.SUBSCRIBER,
            actions=self._READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        # Subscription subscriber permissions
        items.append(Permission(
            collection=constants.CollectionName.SUBSCRIPTION,
            group=constants.CollectionGroup.SUBSCRIPTION,
            role=constants.RoleType.SUBSCRIBER,
            actions=self._NO_ACTIONS,
            portfolio=portfolio
        ))

        # Position subscriber permissions
        items.append(Permission(
            collection=constants.CollectionName.OPEN_POSITION,
            group=constants.CollectionGroup.POSITION,
            role=constants.RoleType.SUBSCRIBER,
            actions=self._READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.CLOSED_POSITION,
            group=constants.CollectionGroup.POSITION,
            role=constants.RoleType.SUBSCRIBER,
            actions=self._READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        # Order subscriber permissions
        items.append(Permission(
            collection=constants.CollectionName.FILLED_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.SUBSCRIBER,
            actions=self._READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.PARTIAL_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.SUBSCRIBER,
            actions=self._READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.PENDING_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.SUBSCRIBER,
            actions=self._READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.CANCELLED_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.SUBSCRIBER,
            actions=self._READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        #########################
        ##  Guest Permissions  ##
        #########################

        # Portfolio guest permissions
        items.append(Permission(
            collection=constants.CollectionName.PORTFOLIO,
            group=constants.CollectionGroup.PORTFOLIO,
            role=constants.RoleType.GUEST,
            actions=self._READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        # Permission guest permissions
        items.append(Permission(
            collection=constants.CollectionName.PERMISSION,
            group=constants.CollectionGroup.PERMISSION,
            role=constants.RoleType.GUEST,
            actions=self._READ_ONLY_ACTIONS,
            portfolio=portfolio
        ))

        # Subscription guest permissions
        items.append(Permission(
            collection=constants.CollectionName.SUBSCRIPTION,
            group=constants.CollectionGroup.SUBSCRIPTION,
            role=constants.RoleType.GUEST,
            actions=self._NO_ACTIONS,
            portfolio=portfolio
        ))

        # Position guest permissions
        items.append(Permission(
            collection=constants.CollectionName.OPEN_POSITION,
            group=constants.CollectionGroup.POSITION,
            role=constants.RoleType.GUEST,
            actions=self._NO_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.CLOSED_POSITION,
            group=constants.CollectionGroup.POSITION,
            role=constants.RoleType.GUEST,
            actions=self._NO_ACTIONS,
            portfolio=portfolio
        ))

        # Order guest permissions
        items.append(Permission(
            collection=constants.CollectionName.FILLED_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.GUEST,
            actions=self._NO_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.PARTIAL_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.GUEST,
            actions=self._NO_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.PENDING_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.GUEST,
            actions=self._NO_ACTIONS,
            portfolio=portfolio
        ))

        items.append(Permission(
            collection=constants.CollectionName.CANCELLED_ORDER,
            group=constants.CollectionGroup.ORDER,
            role=constants.RoleType.GUEST,
            actions=self._NO_ACTIONS,
            portfolio=portfolio
        ))

        return items


class PortfolioManager(models.Manager['Portfolio']):

    def get_queryset(self) -> PortfolioQuerySet:
        return PortfolioQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> PortfolioQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> PortfolioQuerySet:
        return super().filter(*args, **kwargs)


class SubscriptionManager(models.Manager['Subscription']):

    def get_queryset(self) -> SubscriptionQuerySet:
        return SubscriptionQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self) -> SubscriptionQuerySet:
        return super().all()

    def filter(self, *args: typing.Any, **kwargs: typing.Any) -> SubscriptionQuerySet:
        return super().filter(*args, **kwargs)


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

    objects: PortfolioManager = PortfolioManager()

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
        choices=constants.CollectionName.choices,
        default=constants.CollectionName.PORTFOLIO,
    )

    group = models.CharField(
        max_length=15,
        choices=constants.CollectionGroup.choices,
        default=constants.CollectionGroup.PORTFOLIO,
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

    objects: PermissionManager = PermissionManager()

    class Meta:
        ordering = ['role', 'group', 'collection']

    def __str__(self):
        return "%s %s" % (self.role, self.collection)


class Subscription(models.Model):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    role = models.CharField(
        max_length=10,
        choices=constants.RoleType.choices,
        default=constants.RoleType.OWNER,
    )

    objects: SubscriptionManager = SubscriptionManager()

    def __str__(self):
        return "%s %s" % (self.user.username, self.portfolio.code)
