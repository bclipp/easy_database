from unittest.mock import Mock
from unittest.mock import patch

import pandas as pd

import easydb.database as db


def test_connect_disconnect():
    """
    This test is to verify the send_sql method works functionally without a easydb.
    export POSTGRES_DB=testing1234
    export POSTGRES_USER=testing1234
    export POSTGRES_PASSWORD=testing1234
    export DB_IP_ADDRESS=127.0.0.1
    """
    username = "projectetl"
    password = "projectetl"
    hostname = "127.0.0.1"
    database = "projectetl"
    # table = "testing1234"
    connection_string: str = f"""postgresql://{hostname}/{database}?user={username}&password={password}"""
    database_manager = db.DatabaseManager(connection_string)
    database_manager.connect_db()
    database_manager.close_conn()


def test_receive_sql_fetchall():
    """
    This test is to verify the send_sql method works functionally without a easydb.
    export POSTGRES_DB=testing1234
    export POSTGRES_USER=testing1234
    export POSTGRES_PASSWORD=testing1234
    export DB_IP_ADDRESS=127.0.0.1
    """
    username = "projectetl"
    password = "projectetl"
    hostname = "127.0.0.1"
    database = "projectetl"
    # table = "testing1234"
    connection_string: str = f"""postgresql://{hostname}/{database}?user={username}&password={password}"""
    database_manager = db.DatabaseManager(connection_string)
    database_manager.connect_db()
    data_frame:pd.DataFrame = database_manager.receive_sql_fetchall("SELECT * FROM test;")
    print(data_frame)
    database_manager.close_conn()
