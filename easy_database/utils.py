"""
This module holds general reusable functions
"""
import os
from typing import TypedDict, Optional

import pytest

import easy_database.database as db


class ConfigVars(TypedDict):
    """
    Used to define the dict types in a strict way.
    """
    integration_test: Optional[str]


def get_variables() -> ConfigVars:
    """
    get_variables is used to access environmental variables
    :return:
    """
    try:
        integration_test = os.environ.get('INTEGRATION_TEST', default=None)
    except KeyError:
        raise KeyError("Please verify that the needed env variables are set")
    return {"integration_test": integration_test}


def check_integration_test():
    """
    check_integration_test is used for integration tests to avoid running them
    when running unit tests
    :return:
    """
    config: ConfigVars = get_variables()
    if config.get("integration_test") is None:
        pytest.skip("Not an Integration Test")


class BadDatabaseType(Exception):
    """
    This is used for a custom Exception
    """


def database_factory(database_type: str,
                     connection_string: str) -> db.DatabaseManager:
    """

    :param database_type:
    :param connection_string:
    :return:
    """
    if database_type == " postgresql":
        return db.PostgreSQLManger(connection_string)
    raise BadDatabaseType("The Database is not currently supported.")
