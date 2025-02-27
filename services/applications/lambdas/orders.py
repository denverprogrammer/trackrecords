import logging
from pprint import pprint
from typing import Any

from awslambdaric.lambda_context import LambdaContext
from lambdas.services import setup_django

# from vega.models import Order

setup_django()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def created_event(event: dict[Any, Any], context: LambdaContext) -> dict[str, Any]:
    # items = Order.objects.all()
    items = [" testing lsdkjfalskdfjskaldfjaslkdfjslkjf "]
    pprint(event)
    pprint(context)
    pprint(items)
    # Your logic here
    return {"statusCode": 201, "body": "Order created"}


def updated_event(event: dict[Any, Any], context: LambdaContext) -> dict[str, Any]:
    # Your logic here
    return {"statusCode": 200, "body": "Order updated"}


def deleted_event(event: dict[Any, Any], context: LambdaContext) -> dict[str, Any]:
    # Your logic here
    return {"statusCode": 202, "body": "Order deleted"}
