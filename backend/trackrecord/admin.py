from core import constants
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from subadmin import RootSubAdmin, SubAdmin

from .models import Order, Portfolio, Position


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
    subadmins = [PositionSubAdmin, OrderSubAdmin]

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
