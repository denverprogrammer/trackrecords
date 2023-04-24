from core import constants
from django.contrib import admin
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from subadmin import RootSubAdmin, SubAdmin

from .models import Order, Permission, Portfolio, Position


class PermissionSubAdmin(SubAdmin):
    model = Permission

    list_display = ('collection', 'role', 'actions')

    def order_permissions(self, portfolio: Portfolio):
        _CREATE = constants.ActionType.CREATE
        _UPDATE = constants.ActionType.UPDATE
        _VIEW = constants.ActionType.VIEW
        _LIST = constants.ActionType.LIST
        _DELETE = constants.ActionType.DELETE

        permission = Permission()
        permission.collection = constants.CollectionType.FILLED_ORDER
        permission.role = constants.RoleType.OWNER
        permission.actions = [_CREATE, _UPDATE, _VIEW, _LIST, _DELETE]
        permission.portfolio = portfolio
        permission.save()

        permission = Permission()
        permission.collection = constants.CollectionType.PARTIAL_ORDER
        permission.role = constants.RoleType.OWNER
        permission.actions = [_CREATE, _UPDATE, _VIEW, _LIST, _DELETE]
        permission.portfolio = portfolio
        permission.save()

        permission = Permission()
        permission.collection = constants.CollectionType.PENDING_ORDER
        permission.role = constants.RoleType.OWNER
        permission.actions = [_CREATE, _UPDATE, _VIEW, _LIST, _DELETE]
        permission.portfolio = portfolio
        permission.save()

        permission = Permission()
        permission.collection = constants.CollectionType.CANCELLED_ORDER
        permission.role = constants.RoleType.OWNER
        permission.actions = [_CREATE, _UPDATE, _VIEW, _LIST, _DELETE]
        permission.portfolio = portfolio
        permission.save()

    def save_model(self, request, obj, form, change):
        instance: Portfolio = form.save(commit=False)
        instance.save()
        form.save_m2m()

        print(obj)
        print(instance)

        _CREATE = constants.ActionType.CREATE
        _UPDATE = constants.ActionType.UPDATE
        _VIEW = constants.ActionType.VIEW
        _LIST = constants.ActionType.LIST
        _DELETE = constants.ActionType.DELETE

        if not change:
            permission = Permission()
            permission.collection = constants.CollectionType.PORTFOLIO
            permission.role = constants.RoleType.OWNER
            permission.actions = [_UPDATE, _VIEW, _LIST, _DELETE]
            permission.portfolio = obj
            permission.save()

            permission = Permission()
            permission.collection = constants.CollectionType.PERMISSION
            permission.role = constants.RoleType.OWNER
            permission.actions = [_UPDATE, _VIEW, _LIST]
            permission.portfolio = obj
            permission.save()

            permission = Permission()
            permission.collection = constants.CollectionType.SUBSCRIPTION
            permission.role = constants.RoleType.OWNER
            permission.actions = [_CREATE, _UPDATE, _VIEW, _LIST, _DELETE]
            permission.portfolio = obj
            permission.save()

            permission = Permission()
            permission.collection = constants.CollectionType.OPEN_POSITION
            permission.role = constants.RoleType.OWNER
            permission.actions = [_CREATE, _UPDATE, _VIEW, _LIST, _DELETE]
            permission.portfolio = obj
            permission.save()

            permission = Permission()
            permission.collection = constants.CollectionType.CLOSED_POSITION
            permission.role = constants.RoleType.OWNER
            permission.actions = [_CREATE, _UPDATE, _VIEW, _LIST, _DELETE]
            permission.portfolio = obj
            permission.save()

            if instance.record_type is constants.RecordType.ORDER:
                self.order_permissions(obj)

        if change and obj and obj.record_type is not instance.record_type:
            if instance.record_type is constants.RecordType.ORDER:
                self.order_permissions(obj)
            else:
                query = Q(collection__in=[
                    constants.CollectionType.FILLED_ORDER,
                    constants.CollectionType.PARTIAL_ORDER,
                    constants.CollectionType.PENDING_ORDER,
                    constants.CollectionType.CANCELLED_ORDER
                ])
                instance.permissions.filter(query).delete()

        return instance


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
    subadmins = [PermissionSubAdmin, PositionSubAdmin, OrderSubAdmin]

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
            'fields': ('code', 'description', 'initial_capital', 'record_type', 'entry_type')
        }),
        ('Calculations', {
            'fields': ('avg_profit', 'avg_duration', 'win_ratio', 'total_cagr')
        })
    )
