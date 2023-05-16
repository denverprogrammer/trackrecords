import threading
import traceback
from urllib.parse import urlparse

from core import constants
from core.models import Portfolio
from core.patterns import MemStorage
from django.contrib.admin.utils import unquote
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import resolve


class PermissionMiddleware:
    memStorage = None

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.memStorage = MemStorage()

    def setStorage(self, id: str | None, request: HttpRequest) -> None:
        id = int(unquote(id))
        portfolio: Portfolio = Portfolio.objects.get(pk=id) if id else None
        subscription = None
        permissions = []

        if portfolio and request.user.is_authenticated:
            user_query = Q(user__username=request.user.username)
            try:
                subscription = portfolio.subscriptions.get(user_query)
            except:
                pass

        role_type = subscription.role if subscription else constants.Role_Type.GUEST

        if portfolio:
            role_query = Q(role=role_type)
            permissions = list(portfolio.permissions.filter(role_query))

        self.memStorage.portfolio = portfolio
        self.memStorage.subscription = subscription
        self.memStorage.permissions = permissions
        print('storage set $$$$$$$$$$$$$$$$$$$$$$$$$$')

    def __call__(self, request: HttpRequest) -> HttpResponse:
        print('setup storage=========================')

        try:
            matched = resolve(request.path_info)
            name = matched.url_name
            args = matched.args
            kwargs = matched.kwargs

            print({
                'user': request.user.username,
                'name': name,
                'args': args,
                'kwargs': kwargs
            })

            match name:
                case 'trackrecord_portfolio_add' | 'trackrecord_portfolio_changelist':
                    print('portfolio no args and ignored')
                case 'trackrecord_portfolio_change' | 'trackrecord_portfolio_delete':
                    print('portfolio with kwargs')
                    self.setStorage(kwargs['object_id'], request)

                case 'trackrecord_portfolio_order_add' | 'trackrecord_portfolio_order_changelist' | 'trackrecord_portfolio_order_change' | 'trackrecord_portfolio_order_delete':
                    print('orders with args')
                    self.setStorage(args[0], request)

                case 'trackrecord_portfolio_position_add' | 'trackrecord_portfolio_position_changelist' | 'trackrecord_portfolio_position_change' | 'trackrecord_portfolio_position_delete':
                    print('positions with args')
                    self.setStorage(args[0], request)

                case 'trackrecord_portfolio_permission_add' | 'trackrecord_portfolio_permission_delete':
                    print('portfolio with args and ignored')
                case 'trackrecord_portfolio_permission_changelist' | 'trackrecord_portfolio_permission_change':
                    print('permissions with args')
                    self.setStorage(args[0], request)

                case 'trackrecord_portfolio_subscription_add' | 'trackrecord_portfolio_subscription_changelist' | 'trackrecord_portfolio_subscription_change' | 'trackrecord_portfolio_subscription_delete':
                    print('subscriptions with args')
                    self.setStorage(args[0], request)

        except Exception as ex:
            traceback.print_exc()

        print('before response')
        response = self.get_response(request)
        print('After response')

        return response
