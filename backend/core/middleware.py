import threading
import traceback
from urllib.parse import urlparse

from core.models import Portfolio
from core.patterns import MemStorage
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

        if not id or not request.user.is_authenticated:
            return

        portfolio: Portfolio = Portfolio.objects.get(pk=int(id))
        subscription = None
        permissions = []

        if portfolio and request.user.is_authenticated:
            user_query = Q(user__username=request.user.username)
            subscription = portfolio.subscriptions.get(user_query)

        if portfolio and subscription:
            role_query = Q(role=subscription.role)
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
                case 'trackrecord_portfolio_add':
                    pass
                case 'trackrecord_portfolio_changelist':
                    pass
                case 'trackrecord_portfolio_change':
                    print('portfolio change')
                    self.setStorage(kwargs['object_id'], request)
                case 'trackrecord_portfolio_delete':
                    print('portfolio delete')
                    self.setStorage(kwargs['object_id'], request)

                case 'trackrecord_portfolio_order_add':
                    print('orders add')
                    self.setStorage(args[0], request)
                case 'trackrecord_portfolio_order_changelist':
                    print('orders list')
                    self.setStorage(args[0], request)
                case 'trackrecord_portfolio_order_change':
                    print('orders change')
                    self.setStorage(args[0], request)
                case 'trackrecord_portfolio_order_delete':
                    print('orders delete')
                    self.setStorage(args[0], request)

                case 'trackrecord_portfolio_position_add':
                    print('positions add')
                    self.setStorage(args[0], request)
                case 'trackrecord_portfolio_position_changelist':
                    print('positions list')
                    self.setStorage(args[0], request)
                case 'trackrecord_portfolio_position_change':
                    print('positions change')
                    self.setStorage(args[0], request)
                case 'trackrecord_portfolio_position_delete':
                    print('positions delete')
                    self.setStorage(args[0], request)

                case 'trackrecord_portfolio_permission_add':
                    pass
                case 'trackrecord_portfolio_permission_changelist':
                    print('permissions list')
                    self.setStorage(args[0], request)
                case 'trackrecord_portfolio_permission_change':
                    print('permissions change')
                    self.setStorage(args[0], request)
                case 'trackrecord_portfolio_permission_delete':
                    pass

                case 'trackrecord_portfolio_subscription_add':
                    print('subscriptions add')
                    self.setStorage(args[0], request)
                case 'trackrecord_portfolio_subscription_changelist':
                    print('subscriptions list')
                    self.setStorage(args[0], request)
                case 'trackrecord_portfolio_subscription_change':
                    print('subscriptions change')
                    self.setStorage(args[0], request)
                case 'trackrecord_portfolio_subscription_delete':
                    print('subscriptions delete')
                    self.setStorage(args[0], request)

        except Exception as ex:
            traceback.print_exc()

        print('before response')
        response = self.get_response(request)
        print('After response')

        return response
