CHANGELOG
=========

.. towncrier release notes start

2.2.0 (2023-02-27)
==================

Breaking changes
----------------

- Dropped support for Python 3.7 due to using TypeDict for configuration. (`#1127 <https://https://github.com/ClearcodeHQ/pytest-dynamodb/issues/1127>`_)


Features
--------

- Support python 3.10 (`#939 <https://https://github.com/ClearcodeHQ/pytest-dynamodb/issues/939>`_)
- Add support for Python 3.11 (`#1116 <https://https://github.com/ClearcodeHQ/pytest-dynamodb/issues/1116>`_)
- Added typing and check code with mypy.
  Also configuration is being TypeChecked with TypeDict. (`#1127 <https://https://github.com/ClearcodeHQ/pytest-dynamodb/issues/1127>`_)


Miscellaneus
------------

- Fix broken link to dynamodb documentation - introduce delays (`#846 <https://https://github.com/ClearcodeHQ/pytest-dynamodb/issues/846>`_)
- Add towncrier to manage newsfragments and generate changelog (`#1114 <https://https://github.com/ClearcodeHQ/pytest-dynamodb/issues/1114>`_)
- Migrate development dependency management to pipenv (`#1115 <https://https://github.com/ClearcodeHQ/pytest-dynamodb/issues/1115>`_)
- Add your info here (`#1117 <https://https://github.com/ClearcodeHQ/pytest-dynamodb/issues/1117>`_)
- Add automerge action to use Application authentication. (`#1118 <https://https://github.com/ClearcodeHQ/pytest-dynamodb/issues/1118>`_)
- Use tbump to manage package versioning (`#1119 <https://https://github.com/ClearcodeHQ/pytest-dynamodb/issues/1119>`_)


2.1.0
=====

Misc
----

- Rely on `get_port` functionality delivered by `port_for`
- Migrate CI to github actions
- Support only python 3.7 and up

2.0.1
=====

Bugfix
------

- Adjust for mirakuru 2.2.0 and up

2.0.0
=====

- [feature] Drop support for python 2.7. From now on, only support python 3.6 and up

1.2.0
=====

- [enhancement] ability to configure aws region and credentials,

    .. note::

        apparently local dynamo operates on these so whatever you'll set when creating table,
        is whatever is required when accessing the table

1.1.1
=====

- [enhancement] removed path.py dependency

1.1.0
=====

- [enhancement] change deprecated getfuncargvalaue to getfixturevalues, require at least pytest 3.0.0

1.0.1
=====

- [enhancements] set executor timeout to 60. By default mirakuru waits indefinitely, which might cause test hangs

1.0.0
=====

- create command line and pytest.ini configuration options for introducing delays
- create command line and pytest.ini configuration options for dynamodb_dir
- create command line and pytest.ini configuration options for host
- create command line and pytest.ini configuration options for port
- Extracted code from pytest-dbfixtures
