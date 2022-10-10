"""Tests main conftest file."""
from pytest_dynamodb import factories

# pylint:disable=invalid-name
dynamodb_same = factories.dynamodb("dynamodb_proc")
dynamodb_diff = factories.dynamodb(
    "dynamodb_proc",
    access_key="denied_key",
    secret_key="public_key",
    region="eu-west-1",
)
# pylint:enable=invalid-name
