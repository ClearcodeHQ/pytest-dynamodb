# Copyright (C) 2016 by Clearcode <http://clearcode.cc>
# and associates (see AUTHORS).

# This file is part of pytest-dynamodb.

# pytest-dynamodb is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pytest-dynamodb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with pytest-dynamodb. If not, see <http://www.gnu.org/licenses/>.
"""Module containing factories for pytest-dynamodb."""
import os

import pytest
import boto3
from mirakuru import TCPExecutor

from pytest_dynamodb.port import get_port


class JarPathException(Exception):
    """
    Exception thrown, i ncase we can't locate dynamodb's dir to run dynamodb.

    We do not know where user has dynamodb jar file.
    So, we want to tell him that he has to provide a path to dynamodb dir.
    """

    pass


def get_config(request):
    """Return a dictionary with config options."""
    config = {}
    options = [
        'dir', 'host', 'port', 'delay', 'aws_access_key',
        'aws_secret_key', 'aws_region',
    ]
    for option in options:
        option_name = 'dynamodb_' + option
        conf = request.config.getoption(option_name) or \
            request.config.getini(option_name)
        config[option] = conf
    return config


def dynamodb_proc(dynamodb_dir=None, host='localhost', port=None, delay=False):
    """
    Process fixture factory for DynamoDB.

    :param str dynamodb_dir: a path to dynamodb dir (without spaces)
    :param str host: hostname
    :param int port: port
    :param bool delay: causes DynamoDB to introduce delays for certain
        operations

    .. note::
        For more information visit:
            http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html

    :return: function which makes a DynamoDB process
    """
    @pytest.fixture(scope='session')
    def dynamodb_proc_fixture(request):
        """
        Process fixture for DynamoDB.

        It starts DynamoDB when first used and stops it at the end
        of the tests. Works on ``DynamoDBLocal.jar``.

        :param FixtureRequest request: fixture request object
        :rtype: pytest_dbfixtures.executors.TCPExecutor
        :returns: tcp executor
        """
        config = get_config(request)
        path_dynamodb_jar = os.path.join(
            (dynamodb_dir or config['dir']),
            'DynamoDBLocal.jar'
        )

        if not os.path.isfile(path_dynamodb_jar):
            raise JarPathException(
                'You have to provide a path to the dir with dynamodb jar file.'
            )

        dynamodb_port = get_port(port or config['port'])
        dynamodb_delay = delay or config['delay']
        dynamodb_host = host or config['host']

        dynamodb_executor = TCPExecutor(
            '''java
            -Djava.library.path=./DynamoDBLocal_lib
            -jar {path_dynamodb_jar}
            -inMemory
            {delay}
            -port {port}'''
            .format(
                path_dynamodb_jar=path_dynamodb_jar,
                port=dynamodb_port,
                delay='-delayTransientStatuses' if dynamodb_delay else '',
            ),
            host=dynamodb_host,
            port=dynamodb_port,
            timeout=60,
        )
        dynamodb_executor.start()
        request.addfinalizer(dynamodb_executor.stop)
        return dynamodb_executor
    return dynamodb_proc_fixture


def dynamodb(
    process_fixture_name, access_key=None, secret_key=None, region=None
):
    """
    Fixture factory for DynamoDB resource.

    :param str process_fixture_name: name of the process fixture
    :param str access_key: AWS acccess key
    :param str secret_key: AWS secret key
    :param str region: AWS region name
    :rtype: func
    :returns: function which makes a connection to DynamoDB
    """
    @pytest.fixture
    def dynamodb_factory(request):
        """
        Fixture for DynamoDB resource.

        :param FixtureRequest request: fixture request object
        :rtype: Subclass of :py:class:`~boto3.resources.base.ServiceResource`
            https://boto3.readthedocs.io/en/latest/reference/services/dynamodb.html#DynamoDB.Client
        :returns: connection to DynamoDB database
        """
        proc_fixture = request.getfixturevalue(process_fixture_name)
        config = get_config(request)

        dynamo_db = boto3.resource(
            'dynamodb',
            endpoint_url='http://{host}:{port}'.format(
                host=proc_fixture.host,
                port=proc_fixture.port,
                ),
            aws_access_key_id=access_key or config['aws_access_key'],
            aws_secret_access_key=secret_key or config['aws_secret_key'],
            region_name=region or config['aws_region'],
        )

        # remove all tables
        request.addfinalizer(
            lambda: [t.delete() for t in dynamo_db.tables.all()]
        )

        return dynamo_db
    return dynamodb_factory


__all__ = ('dynamodb_proc', 'dynamodb')
