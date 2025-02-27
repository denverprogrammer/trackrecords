
import datetime
import json
import threading
import typing
import uuid

import boto3
from vega.constants import ActionType, CollectionName
from vega.models import Permission, Portfolio, Subscription
from vega.models._ModelStubs import EventBridgeStub


class MembershipManagement:
    _instance = None

    _lock = threading.Lock()

    _values = {
        'portfolio': None,
        'subscription': None,
        'permissions': []
    }

    def __new__(cls):
        if cls._instance is None:
            print('Creating membership storage object')
            with cls._lock:
                # Another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def has_value(self, key: str) -> bool:
        return key in self._values.keys

    @property
    def values(self, key: str) -> object:
        return self._values[key]

    @property
    def portfolio(self) -> Portfolio:
        return self._values['portfolio']

    @portfolio.setter
    def portfolio(self, value: Portfolio) -> None:
        self._values['portfolio'] = value

    @property
    def subscription(self) -> Subscription:
        return self._values['subscription']

    @subscription.setter
    def subscription(self, value: Subscription) -> None:
        self._values['subscription'] = value

    @property
    def permissions(self) -> typing.List[Permission]:
        return self._values['permissions']

    @permissions.setter
    def permissions(self, value: typing.List[Permission]) -> None:
        self._values['permissions'] = value

    def has_permissions(self, collections: typing.List[CollectionName], action: ActionType) -> bool:
        for perm in self.permissions:
            if perm.collection in collections and action in perm.actions and perm.enabled:
                return True

        return False
