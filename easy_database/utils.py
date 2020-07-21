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
    db_ip_address: str
    database: str
    username: str
    password: str
    table: str
    integration_test: Optional[str]
    database_type: str


def get_variables() -> ConfigVars:
    """
    get_variables is used to access environmental variables
    :return:
    """
    try:
        db_ip_address = os.environ['DB_IP_ADDRESS']
        database: str = os.environ['DATABASE']
        username: str = os.environ['USERNAME']
        password: str = os.environ['PASSWORD']
        table: str = os.environ["TABLE"]
        integration_test: Optional[str] = os.environ.get('INTEGRATION_TEST', default=None)
        database_type: str = os.environ["DATABASE_TYPE"]
    except KeyError:
        raise KeyError("Please verify that the needed env variables are set")
    return {"db_ip_address": db_ip_address,
            "database": database,
            "username": username,
            "password": password,
            "integration_test": integration_test,
            "table": table,
            "database_type": database_type}


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


def database_factory(database_type: str) -> db.DatabaseManager:
    """

    :param database_type:
    :return:
    """
    if database_type == " postgresql":
        return db.PostgreSQLManger()
    raise BadDatabaseType("The Database is not currently supported.")
