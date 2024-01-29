"""Test module for pytest-dynamodb."""

import uuid

import pytest
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb import DynamoDBServiceResource


def test_dynamodb(dynamodb: DynamoDBServiceResource) -> None:
    """Simple test for DynamoDB.

    # Create a table
    # Put an item
    # Get the item and check the content of this item
    """
    # create a table
    table = dynamodb.create_table(
        TableName="Test",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        ProvisionedThroughput={
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10,
        },
    )

    _id = str(uuid.uuid4())

    # put an item into db
    table.put_item(
        Item={"id": _id, "test_key": "test_value"},
    )

    # get the item
    item = table.get_item(
        Key={
            "id": _id,
        }
    )

    # check the content of the item
    assert item["Item"]["test_key"] == "test_value"


def test_if_tables_does_not_exist(dynamodb: DynamoDBServiceResource) -> None:
    """We should clear this fixture (remove all tables).

    .. note::
        `all` method on tables object creates an iterable of all
        Table resources in the collection.
    """
    assert not list(dynamodb.tables.all())


def test_different_credentials(
    dynamodb_diff: DynamoDBServiceResource,
    dynamodb_same: DynamoDBServiceResource,
    dynamodb: DynamoDBServiceResource,
) -> None:
    """Check error when accessing table with different credentials.

    scan on dynamodb_diff should result in an error,
    while scans on dynamodb and dynamodb_same should pass.
    """
    dynamodb.create_table(
        AttributeDefinitions=[
            {"AttributeName": "string", "AttributeType": "S"},
        ],
        TableName="string",
        KeySchema=[
            {"AttributeName": "string", "KeyType": "HASH"},
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 123,
            "WriteCapacityUnits": 123,
        },
    )

    dynamodb.Table("string").scan()

    with pytest.raises(ClientError):
        dynamodb_diff.Table("string").scan()

    dynamodb.Table("string").scan()
    dynamodb_same.Table("string").scan()
