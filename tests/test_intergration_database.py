"""
This module is used for integration tests to verify functionality with the postgresql database

    export POSTGRES_DB=testing1234
    export POSTGRES_USER=testing1234
    export POSTGRES_PASSWORD=testing1234
    export DB_IP_ADDRESS=127.0.0.1

"""

import pandas as pd

import easydb.database as db


def test_connect_disconnect():
    """
    test_connect_disconnect to verify the send_sql method works functionally without a easydb.
    """
    dbvars = set_db_variables()
    hostname = dbvars["hostname"]
    database = dbvars["database"]
    username = dbvars["username"]
    password = dbvars["password"]
    connection_string: str = \
        f"postgresql://{hostname}/{database}?user={username}&password={password}"
    database_manager = db.DatabaseManager(connection_string)
    database_manager.connect_db()
    database_manager.close_conn()


def test_receive_sql_fetchall():
    """
    test_receive_sql_fetchall is to verify the send_sql method works functionally without a easydb.
    """
    dbvars = set_db_variables()
    hostname = dbvars["hostname"]
    database = dbvars["database"]
    username = dbvars["username"]
    password = dbvars["password"]
    connection_string: str = \
        f"postgresql://{hostname}/{database}?user={username}&password={password}"
    database_manager = db.DatabaseManager(connection_string)
    database_manager.connect_db()
    data_frame: list = database_manager.receive_sql_fetchall(f"SELECT * FROM {table};")
    print(data_frame)
    database_manager.close_conn()


def test_send_sql():
    """
    test_send_sql is to verify the send_sql method works functionally without a easydb.
    """
    dbvars = set_db_variables()
    hostname = dbvars["hostname"]
    database = dbvars["database"]
    username = dbvars["username"]
    password = dbvars["password"]
    table = dbvars["table"]
    connection_string: str = \
        f"postgresql://{hostname}/{database}?user={username}&password={password}"
    database_manager = db.DatabaseManager(connection_string)
    database_manager.connect_db()
    database_manager.send_sql(f"SELECT * FROM {table};")
    database_manager.close_conn()


def test_df_insert():
    """
    test_df_insert is to verify the send_sql method works functionally without a easydb.
    """
    dbvars = set_db_variables()
    hostname = dbvars["hostname"]
    database = dbvars["database"]
    username = dbvars["username"]
    password = dbvars["password"]
    table = dbvars["table"]
    connection_string: str = \
        f"postgresql://{hostname}/{database}?user={username}&password={password}"
    database_manager = db.DatabaseManager(connection_string)
    database_manager.connect_db()
    data_frame = pd.DataFrame({"id": [7000, 8000, 9000, 10000],
                               'first_name': ['brian', 'john', 'mary', 'same'],
                               'last_name': ['brian', 'john', 'mary', 'same'],
                               'email': ['brian', 'john', 'mary', 'same'],
                               'latitude': [1.1, 2.2, 3.3, 4.4],
                               'longitude': [1.1, 2.2, 3.3, 4.4],
                               'block_id': [1, 2, 3, 4],
                               'state_fips': [1, 2, 3, 4],
                               'state_code': ['brian', 'john', 'mary', 'same'],
                               'block_pop': [1, 2, 3, 4]
                               }, columns=['first_name',
                                           'last_name',
                                           "email",
                                           "latitude",
                                           "longitude",
                                           "block_id",
                                           "state_fips",
                                           "state_code",
                                           "block_pop"])
    database_manager.df_insert(data_frame,
                               table)
    database_manager.close_conn()


def set_db_variables():
    dbvars = {"username": "testing1234",
              "password": "testing1234",
              "hostname": "127.0.0.1",
              "database": "testing1234",
              "table": "customers"}
    return dbvars
