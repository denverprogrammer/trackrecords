from core import constants
from django.contrib import admin
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from subadmin import RootSubAdmin, SubAdmin

from .models import Order, Permission, PermissionManager, Portfolio, Position


class PermissionSubAdmin(SubAdmin):
    model = Permission

    list_display = ('collection', 'role', 'actions')

    def save_model(self, request, obj, form, change):
        # instance: Portfolio = form.save(commit=False)
        # instance.save()
        # form.save_m2m()

        print(obj)
        # print(instance)

        manager: PermissionManager = Permission.objects
        items = []

        print('=============== testing permissions ===============')

        if not change and obj.record_type is constants.RecordType.ORDER:
            print('=============== create permissions ===============')
            items = items + manager.default_owner_permissions(obj)
            items = items + manager.default_order_permissions(obj)
        elif change and obj and obj.record_type is constants.RecordType.ORDER:
            print('=============== update permissions ===============')
            items = items + manager.default_order_permissions(obj)
        elif change and obj and obj.record_type is not constants.RecordType.ORDER:
            print('=============== delete permissions ===============')
            obj.permissions.filter(collection__in=manager._ALL).delete()

        if items.count() > 0:
            print('=============== bulk create permissions ===============')
            manager.bulk_create(items, 100, True, False)

        print('=============== finished permissions ===============')

        super(PermissionSubAdmin, self).save_model(request, obj, form, change)


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
