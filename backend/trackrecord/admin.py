import typing
from functools import wraps
from typing import Optional

from core.patterns import MembershipManagement
from django import forms
from django.contrib import admin
from django.http import HttpRequest
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from more_admin_filters import DropdownFilter
from subadmin import RootSubAdmin, SubAdmin
from vega import constants
from vega.documentation import inherit_docstring_from
from vega.models import (
    Order,
    Permission,
    PermissionManager,
    Portfolio,
    Position,
    Subscription,
)


class AuthorizationMixin:
    """
    Mixin class to handle authorization logic for membership-related objects by collections.

    Attributes:
        mgmt (MembershipManagement): Management of membership-related permissions.z
        collections (list): A list of collections related to the permissions being checked.
    """

    mgmt = MembershipManagement()

    collections = []

    def has_view_permission(self, request: HttpRequest, obj: typing.Any | None = ...) -> bool:
        """
        Determines whether the user has view permission for a given object.
        
        If no specific object is provided, it checks the user's module-level permissions.

        Args:
            request (HttpRequest): The HTTP request object containing metadata about the request.
            obj (typing.Any | None): This object is never used here but must be passed.

        Returns:
            bool: True if the user has view permission, False otherwise.
        """

        if obj is None:
            return self.has_module_permission(request)

        test = self.mgmt.has_permissions(
            self.collections,
            constants.ActionType.VIEW
        )
        
        print(f'User can view {self.collections} is {test}')

        return test

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Determines whether the user has permission to add a new object.

        This method checks if the user has the required permissions to add a new object in the system.

        Args:
            request (HttpRequest): The HTTP request object that contains metadata about the request.

        Returns:
            bool: True if the user has permission to add a new object, False otherwise.
        """
        test = self.mgmt.has_permissions(
            self.collections,
            constants.ActionType.CREATE
        )
        print(f'User can add {self.collections} is {test}')

        return test

    def has_change_permission(self, request: HttpRequest, obj: typing.Any | None = ...) -> bool:
        """
        Determines whether the user has permission to update the specified object.

        This method checks if the user has the required permissions to update a collection.

        Args:
            request (HttpRequest): The HTTP request object that contains metadata about the request.
            obj (typing.Any | None): This object is never used here but must be passed.

        Returns:
            bool: True if the user has change permission for the object or module, False otherwise.
        """
        test = self.mgmt.has_permissions(
            self.collections,
            constants.ActionType.UPDATE
        )
        print(f'User can update {self.collections} is {test}')

        return test

    def has_delete_permission(self, request: HttpRequest, obj: typing.Any | None = ...) -> bool:
        """
        Determines whether the user has permission to delete the specified object.

        This method checks if the user has the required permissions to delete an object.

        Args:
            request (HttpRequest): The HTTP request object that contains metadata about the request.
            obj (typing.Any | None): This object is never used here but must be passed.

        Returns:
            bool: True if the user has delete permission for the object or module, False otherwise.
        """
        test = self.mgmt.has_permissions(
            self.collections,
            constants.ActionType.DELETE
        )
        print(f'User can delete {self.collections} is {test}')

        return test


class SubscriptionSubAdmin(AuthorizationMixin, SubAdmin):
    """
    Admin interface for managing Subscription instances.
    """
    
    model = Subscription

    collections = [
        constants.CollectionName.SUBSCRIPTION
    ]

    search_fields = ['user__username']

    list_display = ('user', 'role', 'portfolio')


class PermissionSubAdmin(AuthorizationMixin, SubAdmin):
    """
    Admin interface for managing Permission instances.
    """

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


class OrderSubAdmin(AuthorizationMixin, SubAdmin):
    """
    Admin interface for managing Order instances.
    """

    model = Order

    raw_id_fields = ('symbol',)

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

    @inherit_docstring_from(AuthorizationMixin)
    def has_view_permission(self, request: HttpRequest, obj: typing.Any | None = ...) -> bool:
        if not self.mgmt.portfolio:
            return False

        can_view = super(OrderSubAdmin, self).has_view_permission(request, obj)
        is_order = self.mgmt.portfolio.record_type == constants.RecordType.ORDER

        return is_order and can_view

    @inherit_docstring_from(SubAdmin)
    def save_model(self, request: HttpRequest, obj: Order, form: forms.ModelForm, change: bool):
        Order.objects.update_status(obj)
        Position.objects.set_position(obj)
        super(OrderSubAdmin, self).save_model(request, obj, form, change)
        Position.objects.update_status(obj.position)
        obj.portfolio.positions.update_streaks()
        Portfolio.objects.update_stats(obj.portfolio)


class PositionSubAdmin(AuthorizationMixin, SubAdmin):
    """
    Admin interface for managing Position instances.
    """

    subadmins = [OrderSubAdmin]

    model = Position

    autocomplete_fields = ['symbol']

    collections = [
        constants.CollectionName.OPEN_POSITION,
        constants.CollectionName.CLOSED_POSITION
    ]

    readonly_fields = ['position_status']

    list_display = (
        'symbol',
        'trend_type',
        'position_status',
        'entry_stamp',
        'entry_price',
        'entry_amount',
        'exit_stamp',
        'exit_price',
        'exit_amount',
        'real_pnl',
        'unreal_pnl'
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

    @inherit_docstring_from(SubAdmin)
    def save_model(self, request: HttpRequest, obj: Position, form: forms.ModelForm, change: bool):
        super(PositionSubAdmin, self).save_model(request, obj, form, change)


@admin.register(Portfolio)
class PortfolioAdmin(RootSubAdmin):
    """
    Admin interface for managing Portfolio instances.
    """

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
        'avg_profit_amount',
        'avg_loss_amount',
        'avg_win_duration',
        'avg_loss_duration',
        'win_ratio',
        'total_cagr',
        'total_wins',
        'total_losses',
        'total_washes',
        'total_trades'
    ]

    list_display = (
        'code',
        'description',
        'initial_capital',
        'record_type',
        'entry_type',
        'win_ratio',
        'total_cagr'
    )

    fieldsets = (
        (None, {
            'fields': ('code', 'description', 'initial_capital', 'record_type', 'entry_type', 'allowed_roles')
        }),
        ('Calculations', {
            'fields': (
                'avg_profit_amount',
                'avg_loss_amount',
                'avg_win_duration',
                'avg_loss_duration',
                'win_ratio',
                'total_cagr',
                'total_wins',
                'total_losses',
                'total_washes',
                'total_trades'
            )
        })
    )

    @inherit_docstring_from(SubAdmin)
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
        Portfolio.objects.update_stats(obj)
