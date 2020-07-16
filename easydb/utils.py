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
    postgres_db: str
    postgres_user: str
    postgres_password: str
    integration_test: Optional[str]


def get_variables() -> ConfigVars:
    """
    get_variables is used to access environmental variables
    :return:
    """
    try:
        db_ip_address = os.environ['DB_IP_ADDRESS']
        postgres_db = os.environ['POSTGRES_DB']
        postgres_user = os.environ['POSTGRES_USER']
        postgres_password = os.environ['POSTGRES_PASSWORD']
        integration_test = os.environ.get('INTEGRATION_TEST', default=None)
    except KeyError:
        raise KeyError("Please verify that the needed env variables are set")
    return {"db_ip_address": db_ip_address,
            "postgres_db": postgres_db,
            "postgres_user": postgres_user,
            "postgres_password": postgres_password,
            "integration_test": integration_test}


def check_integration_test():
    """
    check_integration_test is used for integration tests to avoid running them
    when running unit tests
    :return:
    """
    config: ConfigVars = get_variables()
    if config.get("integration_test") is None:
        pytest.skip("Not an Integration Test")
