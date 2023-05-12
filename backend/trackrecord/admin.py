import typing
from typing import Optional

from core import constants
from core.models import (
    Order,
    Permission,
    PermissionManager,
    Portfolio,
    Position,
    Subscription,
)
from core.patterns import MemStorage
from django import forms
from django.contrib import admin
from django.http import HttpRequest
from django.http.request import HttpRequest
from more_admin_filters import DropdownFilter
from subadmin import RootSubAdmin, SubAdmin


class hasAuthorizationMixin:

    memStorage = MemStorage()
    collections = []

    def has_view_permission(self, request: HttpRequest, obj: typing.Any | None = ...) -> bool:
        if obj is None:
            return self.has_module_permission(request)

        print(f'check if user can view {self.collections}')

        test = self.memStorage.has_permissions(
            self.collections,
            constants.ActionType.VIEW
        )
        print(test)

        return test

    def has_add_permission(self, request: HttpRequest) -> bool:
        print(f'check if user can add {self.collections}')

        test = self.memStorage.has_permissions(
            self.collections,
            constants.ActionType.CREATE
        )
        print(test)

        return test

    def has_change_permission(self, request: HttpRequest, obj: typing.Any | None = ...) -> bool:
        print(f'check if user can update {self.collections}')

        test = self.memStorage.has_permissions(
            self.collections,
            constants.ActionType.UPDATE
        )
        print(test)

        return test

    def has_delete_permission(self, request: HttpRequest, obj: typing.Any | None = ...) -> bool:
        print(f'check if user can delete {self.collections}')

        test = self.memStorage.has_permissions(
            self.collections,
            constants.ActionType.DELETE
        )
        print(test)

        return test

    def has_module_permission(self, request: HttpRequest | None) -> bool:
        print(f'check if user can list {self.collections}')

        test = self.memStorage.has_permissions(
            self.collections,
            constants.ActionType.LIST
        )
        print(test)

        return test


class SubscriptionSubAdmin(hasAuthorizationMixin, SubAdmin):
    model = Subscription

    collections = [
        constants.CollectionName.SUBSCRIPTION
    ]

    search_fields = ['user__username']

    list_display = ('user', 'role', 'portfolio')


class PermissionSubAdmin(hasAuthorizationMixin, SubAdmin):
    model = Permission

    collections = [
        constants.CollectionName.PERMISSION
    ]

    list_display = ('role', 'group', 'collection', 'actions', 'enabled')

    list_filter = (
        ('enabled', DropdownFilter),
        ('role', DropdownFilter),
        ('group', DropdownFilter),
        ('collection', DropdownFilter),
    )

    readonly_fields = [
        'collection',
        'role',
        'group',
        'enabled',
    ]


class OrderSubAdmin(hasAuthorizationMixin, SubAdmin):

    model = Order

    autocomplete_fields = ['symbol']

    collections = [
        constants.CollectionName.FILLED_ORDER,
        constants.CollectionName.PARTIAL_ORDER,
        constants.CollectionName.PENDING_ORDER,
        constants.CollectionName.CANCELLED_ORDER
    ]

    list_display = (
        'symbol',
        'order_type',
        'order_action',
        'order_status',
        'sent_stamp',
        'sent_price',
        'limit_price',
        'sent_amount',
        'filled_stamp',
        'filled_price',
        'filled_amount'
    )

    fieldsets = (
        (None, {
            'fields': ('symbol', 'order_type', 'order_action')
        }),
        ('Sent Order', {
            'fields': ('sent_stamp', 'sent_price', 'limit_price', 'sent_amount')
        }),
        ('Filled Order', {
            'fields': ('filled_stamp', 'filled_price', 'filled_amount')
        })
    )

    def has_view_permission(self, request: HttpRequest, obj: typing.Any | None = ...) -> bool:
        print('order module permissions ###########################')

        if not self.memStorage.portfolio:
            return False

        can_view = super(OrderSubAdmin, self).has_view_permission(request, obj)
        is_order = self.memStorage.portfolio.record_type == constants.RecordType.ORDER

        print({
            'can_view': can_view,
            'is_order': is_order
        })

        return is_order and can_view

    def save_model(self, request: HttpRequest, obj: Order, form: forms.ModelForm, change: bool):
        super(OrderSubAdmin, self).save_model(request, obj, form, change)

        # print(obj.position)
        # print(obj.position.orders)


class PositionSubAdmin(hasAuthorizationMixin, SubAdmin):
    subadmins = [OrderSubAdmin]

    model = Position

    autocomplete_fields = ['symbol']

    collections = [
        constants.CollectionName.OPEN_POSITION,
        constants.CollectionName.CLOSED_POSITION
    ]

    list_display = (
        'symbol',
        'trend_type',
        'position_status',
        'entry_stamp',
        'entry_price',
        'entry_amount',
        'exit_stamp',
        'exit_price',
        'exit_amount'
    )

    fieldsets = (
        (None, {
            'fields': ('symbol', 'trend_type', 'position_status')
        }),
        ('Entry Order', {
            'fields': ('entry_stamp', 'entry_price', 'entry_amount')
        }),
        ('Exit Order', {
            'fields': ('exit_stamp', 'exit_price', 'exit_amount')
        })
    )

    def save_model(self, request: HttpRequest, obj: Position, form: forms.ModelForm, change: bool):
        super(PositionSubAdmin, self).save_model(request, obj, form, change)


@admin.register(Portfolio)
class PortfolioAdmin(hasAuthorizationMixin, RootSubAdmin):

    subadmins = [
        PermissionSubAdmin,
        SubscriptionSubAdmin,
        PositionSubAdmin,
        OrderSubAdmin
    ]

    collections = [
        constants.CollectionName.PORTFOLIO
    ]

    search_fields = ['code', 'description']

    readonly_fields = [
        'avg_profit',
        'avg_duration',
        'win_ratio',
        'total_cagr'
    ]

    list_display = (
        'code',
        'description',
        'initial_capital',
        'record_type',
        'entry_type',
        'avg_profit',
        'avg_duration',
        'win_ratio',
        'total_cagr'
    )

    fieldsets = (
        (None, {
            'fields': ('code', 'description', 'initial_capital', 'record_type', 'entry_type', 'allowed_roles')
        }),
        ('Calculations', {
            'fields': ('avg_profit', 'avg_duration', 'win_ratio', 'total_cagr')
        })
    )

    def has_module_permission(self, request: HttpRequest) -> bool:
        return True

    def has_add_permission(self, request: HttpRequest) -> bool:
        return True

    def has_view_permission(self, request: HttpRequest, obj: typing.Any | None = ...) -> bool:
        if obj is None:
            return True

        return super().has_view_permission(request, obj)

    def save_model(self, request: HttpRequest, obj: Portfolio, form: forms.ModelForm, change: bool):
        super(PortfolioAdmin, self).save_model(request, obj, form, change)
        manager: PermissionManager = Permission.objects

        if not change:
            subscription = Subscription()
            subscription.portfolio = obj
            subscription.user = request.user
            subscription.role = constants.RoleType.OWNER
            subscription.save()
            items = manager.default_owner_permissions(obj)
            items += manager.default_admin_permissions(obj)
            items += manager.default_subscription_permissions(obj)
            items += manager.default_guest_permissions(obj)
            manager.bulk_create(items, None, True)

        permissions = manager.all().filter(portfolio__id=obj.id)

        for item in permissions:
            is_order_record = obj.record_type == constants.RecordType.ORDER
            is_order_group = item.group == constants.CollectionGroup.ORDERS
            item.enabled = item.role in obj.allowed_roles

            if not is_order_record and is_order_group:
                item.enabled = False

        manager.bulk_update(permissions, ['enabled'])
