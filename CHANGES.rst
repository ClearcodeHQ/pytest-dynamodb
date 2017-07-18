CHANGELOG
=========

1.2.0
-------

- [enhancement] ability to configure aws region and credentials,

    .. note::

        apparently local dynamo operates on these so whatever you'll set when creating table,
        is whatever is required when accessing the table

1.1.1
-------

- [enhancement] removed path.py dependency

1.1.0
-------

- [enhancement] change deprecated getfuncargvalaue to getfixturevalues, require at least pytest 3.0.0

1.0.1
-------

- [enhancements] set executor timeout to 60. By default mirakuru waits indefinitely, which might cause test hangs

1.0.0
-------

- create command line and pytest.ini configuration options for introducing delays
- create command line and pytest.ini configuration options for dynamodb_dir
- create command line and pytest.ini configuration options for host
- create command line and pytest.ini configuration options for port
- Extracted code from pytest-dbfixtures
