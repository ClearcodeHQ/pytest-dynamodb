"""Tests main conftest file."""
from pytest_dynamodb.plugin import *
from pytest_dynamodb import factories

# pylint:disable=invalid-name
dynamodb_same = factories.dynamodb("dynamodb_proc")
dynamodb_diff = factories.dynamodb(
    "dynamodb_proc",
    access_key="fakeDeniedKeyId",
    secret_key="fakeDeniedSecretAccessKey",
)
# pylint:enable=invalid-name
