
import datetime
import json
import threading
import typing
import uuid

import boto3
from vega.constants import ActionType, CollectionName
from vega.models import Permission, Portfolio, Subscription
from vega.models._ModelStubs import EventBridgeStub


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
