import typing

from core import constants
from django import forms
from django.contrib import admin
from django.http import HttpRequest
from more_admin_filters import DropdownFilter
from subadmin import RootSubAdmin, SubAdmin

from .models import (
    Order,
    Permission,
    PermissionManager,
    Portfolio,
    Position,
    Subscription,
)


class SubscriptionSubAdmin(SubAdmin):
    model = Subscription

    search_fields = ['user__username']

    list_display = ('user', 'role', 'portfolio')


class PermissionSubAdmin(SubAdmin):
    model = Permission

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

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: typing.Any | None = ...) -> bool:
        return False


class OrderSubAdmin(SubAdmin):
    model = Order

    autocomplete_fields = ['symbol']

    list_display = (
        'symbol',
        'order_type',
        'order_action',
        'order_status',
        'sent_stamp',
        'sent_price',
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
            'fields': ('sent_stamp', 'sent_price', 'sent_amount')
        }),
        ('Filled Order', {
            'fields': ('filled_stamp', 'filled_price', 'filled_amount')
        })
    )


class PositionSubAdmin(SubAdmin):
    subadmins = [OrderSubAdmin]

    model = Position

    search_fields = ['symbol']

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


@admin.register(Portfolio)
class PortfolioAdmin(RootSubAdmin):
    subadmins = [
        PermissionSubAdmin,
        SubscriptionSubAdmin,
        PositionSubAdmin,
        OrderSubAdmin
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

    def save_model(self, request: HttpRequest, obj: Portfolio, form: forms.ModelForm, change: bool):
        super(PortfolioAdmin, self).save_model(request, obj, form, change)

        manager: PermissionManager = Permission.objects

        if not change:
            subscription = Subscription()
            subscription.portfolio = obj
            subscription.user = request.user
            subscription.role = constants.RoleType.OWNER
            subscription.save()
            items = manager.default_permissions(obj)
            manager.bulk_create(items, None, True)

        permissions = manager.all().filter(portfolio__id=obj.id)

        for item in permissions:
            is_order_record = obj.record_type == constants.RecordType.ORDER
            is_order_group = item.group == constants.CollectionGroup.ORDER
            item.enabled = item.role in obj.allowed_roles

            if not is_order_record and is_order_group:
                item.enabled = False

        manager.bulk_update(permissions, ['enabled'])
