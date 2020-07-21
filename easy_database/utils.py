"""
This module holds general reusable functions
"""
import os
from typing import TypedDict, Optional

import pytest


class ConfigVars(TypedDict):
    """
    Used to define the dict types in a strict way.
    """
    db_ip_address: str
    database: str
    username: str
    password: str
    table: Optional[str]
    integration_test: Optional[str]
    database_type: Optional[str]


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
        table: Optional[str] = os.environ.get('TABLE', default=None)
        integration_test: Optional[str] = os.environ.get('INTEGRATION_TEST', default=None)
        database_type: Optional[str] = os.environ.get('DATABASE_TYPE', default=None)
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
        print("Not an Integration Test")
        pytest.skip("Not an Integration Test")
    else:
        print("running unit test")
