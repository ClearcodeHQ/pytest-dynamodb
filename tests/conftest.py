"""Tests main conftest file."""
import sys
import os
import warnings

import pytest

major, minor = sys.version_info[:2]

if not (major >= 3 and minor >= 5):
    warnings.simplefilter("error", category=DeprecationWarning)


@pytest.fixture()
def aws_config():
    """Set AWS config options in environment variables."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'access_key'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'secret_key'
    os.environ['AWS_DEFAULT_REGION'] = 'us-west-1'
