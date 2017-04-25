pytest-dynamodb
===============

.. image:: https://img.shields.io/pypi/v/pytest-dynamodb.svg
    :target: https://pypi.python.org/pypi/pytest-dynamodb/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/wheel/pytest-dynamodb.svg
    :target: https://pypi.python.org/pypi/pytest-dynamodb/
    :alt: Wheel Status

.. image:: https://img.shields.io/pypi/pyversions/pytest-dynamodb.svg
    :target: https://pypi.python.org/pypi/pytest-dynamodb/
    :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/pytest-dynamodb.svg
    :target: https://pypi.python.org/pypi/pytest-dynamodb/
    :alt: License

Package status
--------------

.. image:: https://travis-ci.org/ClearcodeHQ/pytest-dynamodb.svg?branch=v1.1.1
    :target: https://travis-ci.org/ClearcodeHQ/pytest-dynamodb
    :alt: Tests

.. image:: https://coveralls.io/repos/ClearcodeHQ/pytest-dynamodb/badge.png?branch=v1.1.1
    :target: https://coveralls.io/r/ClearcodeHQ/pytest-dynamodb?branch=v1.1.1
    :alt: Coverage Status

.. image:: https://requires.io/github/ClearcodeHQ/pytest-dynamodb/requirements.svg?tag=v1.1.1
     :target: https://requires.io/github/ClearcodeHQ/pytest-dynamodb/requirements/?tag=v1.1.1
     :alt: Requirements Status

What is this?
=============

This is a pytest plugin, that enables you to test your code that relies on a running DynamoDB Database.
It allows you to specify fixtures for DynamoDB process and client (resource in AWS boto terms).


How to use
==========

.. warning::

    Please download the `DynamoDB database locally <http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html>`_.

Plugin contains two fixtures

* **dynamodb** - it's a client/resource fixture that has functional scope. After each test it drops tables in DynamoDB.
* **dynamodb_proc** - session scoped fixture, that starts DynamoDB instance at it's first use and stops at the end of the tests.

Simply include one of these fixtures into your tests fixture list.

You can also create additional dynamodb client and process fixtures if you'd need to:


.. code-block:: python

    from pytest_dynamodb import factories

    dynamodb_my_proc = factories.dynamodb_proc(
        port=None, logsdir='/tmp', delay=True)
    dynamodb_my = factories.dynamodb('dynamodb_my_proc')

.. note::

    Each DynamoDB process fixture can be configured in a different way than the others through the fixture factory arguments.


Configuration
=============

You can define your settings in three ways, it's fixture factory argument, command line option and pytest.ini configuration option.
You can pick which you prefer, but remember that these settings are handled in the following order:

    * ``Fixture factory argument``
    * ``Command line option``
    * ``Configuration option in your pytest.ini file``

+------------------------------------------------------------------------------------------------------------+--------------------------+---------------------+-------------------+---------------+
| DynamoDB option                                                                                            | Fixture factory argument | Command line option | pytest.ini option | Default       |
+============================================================================================================+==========================+=====================+===================+===============+
| Path to dynamodb jar file                                                                                  | dynamodb_dir             | --dynamodb-dir      | dynamodb_dir      | /tmp/dynamodb |
+------------------------------------------------------------------------------------------------------------+--------------------------+---------------------+-------------------+---------------+
| host                                                                                                       | host                     | --dynamodb-host     | dynamodb_host     | 127.0.0.1     |
+------------------------------------------------------------------------------------------------------------+--------------------------+---------------------+-------------------+---------------+
| port                                                                                                       | port                     | --dynamodb-port     | dynamodb_port     | random        |
+------------------------------------------------------------------------------------------------------------+--------------------------+---------------------+-------------------+---------------+
| `Introduce delays <http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)>`_  | delay                    | --dynamodb-delay    | dynamodb_delay    | false         |
+------------------------------------------------------------------------------------------------------------+--------------------------+---------------------+-------------------+---------------+


Example usage:

* pass it as an argument in your own fixture

    .. code-block:: python

        dynamodb_proc = factories.dynamodb_proc(
            port=8888)

* use ``--dynamodb-port`` command line option when you run your tests

    .. code-block::

        py.test tests --dynamodb-port=8888


* specify your port as ``dynamodb_port`` in your ``pytest.ini`` file.

    To do so, put a line like the following under the ``[pytest]`` section of your ``pytest.ini``:

    .. code-block:: ini

        [pytest]
        dynamodb_port = 8888

Package resources
-----------------

* Bug tracker: https://github.com/ClearcodeHQ/pytest-dynamodb/issues
