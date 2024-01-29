"""Tests main conftest file."""

from pytest_dynamodb import factories
from pytest_dynamodb.plugin import *  # noqa: F403

# pylint:disable=invalid-name
dynamodb_same = factories.dynamodb("dynamodb_proc")
dynamodb_diff = factories.dynamodb(
    "dynamodb_proc",
    access_key="fakeDeniedKeyId",
    secret_key="fakeDeniedSecretAccessKey",
)
# pylint:enable=invalid-name
