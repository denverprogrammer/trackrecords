from typing import Any

from awslambdaric.lambda_context import LambdaContext
from lambdas.services import setup_django

setup_django()


def created_event(event: dict[Any, Any], context: LambdaContext) -> dict[str, Any]:
    # Your logic here
    return {"statusCode": 201, "body": "Profile created"}


def updated_event(event: dict[Any, Any], context: LambdaContext) -> dict[str, Any]:
    # Your logic here
    return {"statusCode": 200, "body": "Profile updated"}


def deleted_event(event: dict[Any, Any], context: LambdaContext) -> dict[str, Any]:
    # Your logic here
    return {"statusCode": 202, "body": "Profile deleted"}
