import logging
import os
from pprint import pprint

import django
from awslambdaric.lambda_context import LambdaContext

logger = logging.getLogger()
logger.setLevel(logging.INFO)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from vega.models import Order


def created_event(event: dict, context: LambdaContext) -> dict:
    items = Order.objects.all()
    pprint(event)
    pprint(context)
    # Your logic here
    return {
        'statusCode': 201,
        'body': 'Order created'
    }

def updated_event(event: dict, context: LambdaContext) -> dict:
    # Your logic here
    return {
        'statusCode': 200,
        'body': 'Order updated'
    }
    
def deleted_event(event: dict, context: LambdaContext) -> dict:
    # Your logic here
    return {
        'statusCode': 202,
        'body': 'Order deleted'
    }
