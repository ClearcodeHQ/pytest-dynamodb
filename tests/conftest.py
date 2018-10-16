"""Tests main conftest file."""
import sys
import warnings

from pytest_dynamodb import factories

if not sys.version_info >= (3, 5):
    warnings.simplefilter("error", category=DeprecationWarning)


# pylint:disable=invalid-name
dynamodb_same = factories.dynamodb('dynamodb_proc')
dynamodb_diff = factories.dynamodb(
    'dynamodb_proc', access_key='denied_key', secret_key='public_key'
)
# pylint:enable=invalid-name
