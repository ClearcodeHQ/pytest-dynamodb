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
from pathlib import Path
from typing import Any, Callable, Generator, Optional, TypedDict

import boto3
import pytest
from mirakuru import ProcessExitedWithError, TCPExecutor
from mypy_boto3_dynamodb import DynamoDBServiceResource
from port_for import get_port
from pytest import FixtureRequest


class PytestDynamoDBConfigType(TypedDict):
    """Configuration type dict."""

    dir: Path
    host: str
    port: str
    delay: str
    aws_access_key: str
    aws_secret_key: str
    aws_region: str


class JarPathException(Exception):
    """Exception thrown, i ncase we can't locate dynamodb's dir to run dynamodb.

    We do not know where user has dynamodb jar file.
    So, we want to tell him that he has to provide a path to dynamodb dir.
    """


def get_config(request: FixtureRequest) -> PytestDynamoDBConfigType:
    """Return a dictionary with config options."""

    def get_conf_option(option: str) -> Any:
        option_name = "dynamodb_" + option
        return request.config.getoption(option_name) or request.config.getini(
            option_name
        )

    config: PytestDynamoDBConfigType = {
        "dir": get_conf_option("dir"),
        "host": get_conf_option("host"),
        "port": get_conf_option("port"),
        "delay": get_conf_option("delay"),
        "aws_access_key": get_conf_option("aws_access_key"),
        "aws_secret_key": get_conf_option("aws_secret_key"),
        "aws_region": get_conf_option("aws_region"),
    }
    return config


def dynamodb_proc(
    dynamodb_dir: Optional[str] = None,
    host: str = "localhost",
    port: Optional[int] = None,
    delay: bool = False,
) -> Callable[[FixtureRequest], Any]:
    """Process fixture factory for DynamoDB.

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

    @pytest.fixture(scope="session")
    def dynamodb_proc_fixture(
        request: FixtureRequest,
    ) -> Generator[TCPExecutor, None, None]:
        """Process fixture for DynamoDB.

        It starts DynamoDB when first used and stops it at the end
        of the tests. Works on ``DynamoDBLocal.jar``.

        :param FixtureRequest request: fixture request object
        :rtype: pytest_dbfixtures.executors.TCPExecutor
        :returns: tcp executor
        """
        config = get_config(request)
        path_dynamodb_jar = os.path.join(
            (dynamodb_dir or config["dir"]), "DynamoDBLocal.jar"
        )

        if not os.path.isfile(path_dynamodb_jar):
            raise JarPathException(
                "You have to provide a path to the dir with dynamodb jar file."
            )

        dynamodb_port = get_port(port or config["port"])
        assert dynamodb_port
        dynamodb_delay = (
            "-delayTransientStatuses" if delay or config["delay"] else ""
        )
        dynamodb_host = host or config["host"]
        dynamodb_executor = TCPExecutor(
            f"java -Djava.library.path=./DynamoDBLocal_lib "
            f"-jar {path_dynamodb_jar} "
            f"-inMemory {dynamodb_delay} "
            f"-port {dynamodb_port}",
            host=dynamodb_host,
            port=dynamodb_port,
            timeout=60,
        )
        dynamodb_executor.start()
        yield dynamodb_executor
        try:
            dynamodb_executor.stop()
        except ProcessExitedWithError:
            pass

    return dynamodb_proc_fixture


def dynamodb(
    process_fixture_name: str,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    region: Optional[str] = None,
) -> Callable[[FixtureRequest], Any]:
    """Fixture factory for DynamoDB resource.

    :param str process_fixture_name: name of the process fixture
    :param str access_key: AWS acccess key
    :param str secret_key: AWS secret key
    :param str region: AWS region name
    :rtype: func
    :returns: function which makes a connection to DynamoDB
    """

    @pytest.fixture
    def dynamodb_factory(
        request: FixtureRequest,
    ) -> Generator[DynamoDBServiceResource, None, None]:
        """Fixture for DynamoDB resource.

        :param FixtureRequest request: fixture request object
        :rtype: Subclass of :py:class:`~boto3.resources.base.ServiceResource`
            https://boto3.readthedocs.io/en/latest/reference/services/dynamodb.html#DynamoDB.Client
        :returns: connection to DynamoDB database
        """
        proc_fixture = request.getfixturevalue(process_fixture_name)
        config = get_config(request)

        dynamo_db = boto3.resource(
            "dynamodb",
            endpoint_url=f"http://{proc_fixture.host}:{proc_fixture.port}",
            aws_access_key_id=access_key or config["aws_access_key"],
            aws_secret_access_key=secret_key or config["aws_secret_key"],
            region_name=region or config["aws_region"],
        )

        yield dynamo_db
        for table in dynamo_db.tables.all():  # pylint:disable=no-member
            table.delete()

    return dynamodb_factory


__all__ = ("dynamodb_proc", "dynamodb")
