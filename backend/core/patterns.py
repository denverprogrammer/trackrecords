
import datetime
import json
import threading
import typing
import uuid

import boto3
from core.constants import ActionType, CollectionName
from core.models import Permission, Portfolio, Subscription
from core.models._ModelStubs import EventBridgeStub


class MemStorage:
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


class EventBridge(object):
    _instance = None

    _lock = threading.Lock()

    _client = None

    _events = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating event bridge object')
            cls._instance = super(EventBridge, cls).__new__(cls)
            cls._client = boto3.client('events')
            cls._events = []

        return cls._instance
    
    @staticmethod
    def build_event(source: str, detail_type: str, instance: EventBridgeStub) -> dict:
        return {
            'Time': datetime.datetime.now(),
            'Source': source,
            'Resources': [],
            'DetailType': detail_type,
            'Detail': {
                'id': instance.getId()
            },
            'EventBusName': 'ambient',
            'TraceHeader': uuid.uuid4()
        }

    @staticmethod
    def created_event(source: str, detail_type: str, instance: EventBridgeStub) -> dict:
        return EventBridge.build_event(source, detail_type, instance)
        
    @staticmethod
    def updated_event(source: str, detail_type: str, instance: EventBridgeStub) -> dict:
        return EventBridge.build_event(source, detail_type, instance)
        
    @staticmethod
    def deleted_event(source: str, detail_type: str, instance: EventBridgeStub) -> dict:
        return EventBridge.build_event(source, detail_type, instance)
        
    def save_event(self, event: dict) -> None:
        self._events.append(event)
    
    def send_events(self) -> list:
        items = []
        responses = []

        for event in self._events:
            if not isinstance(event['Detail'], str):
                event['Detail'] = json.dumps(event['Detail'])
                items.append(event)

        if items.length > 0:
            responses.append(self._client.put_events(items))

        return responses
