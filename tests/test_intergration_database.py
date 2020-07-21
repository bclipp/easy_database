"""
This module is used for integration tests to verify functionality with the postgresql database

    export POSTGRES_DB=testing1234
    export POSTGRES_USER=testing1234
    export POSTGRES_PASSWORD=testing1234
    export DB_IP_ADDRESS=127.0.0.1

"""

import pandas as pd

from easy_database import database as db, utils


def test_postgresqlmanager_connect_disconnect():
    """
    test_connect_disconnect to verify the send_sql method works functionally without a easydb.
    """
    utils.check_integration_test()
    dbvars = utils.get_variables()
    database_manager = db.PostgreSQLManger()
    database_manager.set_connection_data(dbvars)
    database_manager.open_conn()
    database_manager.close_conn()


def test_postgresqlmanager_receive_sql_fetchall():
    """
    test_receive_sql_fetchall is to verify the send_sql method works functionally without a easydb.
    """
    utils.check_integration_test()
    dbvars = utils.get_variables()
    database_manager = db.PostgreSQLManger()
    database_manager.set_connection_data(dbvars)
    database_manager.open_conn()
    table = dbvars["table"]
    table_data: list = database_manager.receive_sql_fetchall(f"SELECT * FROM {table};")
    print(table_data)
    database_manager.close_conn()


def test_postgresqlmanager_send_sql():
    """
    test_send_sql is to verify the send_sql method works functionally without a easydb.
    """
    utils.check_integration_test()
    dbvars = utils.get_variables()
    database_manager = db.PostgreSQLManger()
    database_manager.set_connection_data(dbvars)
    database_manager.open_conn()
    table = dbvars["table"]
    database_manager.send_sql(f"SELECT * FROM {table};")
    database_manager.close_conn()


def test_postgresqlmanager_df_insert_no_conflict():
    """
    test_df_insert_no_conflict is to verify the send_sql method works functionally without a easydb.
    """
    utils.check_integration_test()
    dbvars = utils.get_variables()
    database_manager = db.PostgreSQLManger()
    database_manager.set_connection_data(dbvars)
    table = "test_customers"
    database_manager.open_conn()
    data_frame = pd.DataFrame({"id": [700000, 800000, 900000, 1000000],
                               'first_name': ['brian', 'john', 'mary', 'same'],
                               'last_name': ['brian', 'john', 'mary', 'same'],
                               'email': ['brian', 'john', 'mary', 'same'],
                               'latitude': [1.1, 2.2, 3.3, 4.4],
                               'longitude': [1.1, 2.2, 3.3, 4.4],
                               'block_id': [1, 2, 3, 4],
                               'state_fips': [1, 2, 3, 4],
                               'state_code': ['brian', 'john', 'mary', 'same'],
                               'block_pop': [1, 2, 3, 4]
                               }, columns=["id",
                                           'first_name',
                                           'last_name',
                                           "email",
                                           "latitude",
                                           "longitude",
                                           "block_id",
                                           "state_fips",
                                           "state_code",
                                           "block_pop"])
    create_fake_table(database_manager)
    database_manager.df_insert(data_frame,
                               table)
    database_manager.send_sql("DROP TABLE test_customers;")
    database_manager.close_conn()


def test_postgresqlmanager_df_insert_conflict():
    """
    test_df_insert_conflict is to verify the send_sql method works functionally without a easydb.
    """
    utils.check_integration_test()
    dbvars = utils.get_variables()
    database_manager = db.PostgreSQLManger()
    database_manager.set_connection_data(dbvars)
    table = "test_customers"
    database_manager.open_conn()
    data_frame = pd.DataFrame({"id": [9000001, 800001, 2000001, 3000001],
                               'first_name': ['brian', 'john', 'mary', 'same'],
                               'last_name': ['brian', 'john', 'mary', 'same'],
                               'email': ['brian', 'john', 'mary', 'same'],
                               'latitude': [1.1, 2.2, 3.3, 4.4],
                               'longitude': [1.1, 2.2, 3.3, 4.4],
                               'block_id': [1, 2, 3, 4],
                               'state_fips': [1, 2, 3, 4],
                               'state_code': ['brian', 'john', 'mary', 'same'],
                               'block_pop': [1, 2, 3, 4]
                               }, columns=["id",
                                           'first_name',
                                           'last_name',
                                           "email",
                                           "latitude",
                                           "longitude",
                                           "block_id",
                                           "state_fips",
                                           "state_code",
                                           "block_pop"])
    create_fake_table(database_manager)
    database_manager.df_insert(data_frame,
                               table)
    database_manager.df_insert(data_frame,
                               table,
                               conflict_id="id")
    database_manager.send_sql("DROP TABLE test_customers;")
    database_manager.close_conn()


def create_fake_table(database_manager: db.DatabaseManager):
    """
    used to setup table for tests
    :return:
    """
    sql_query: str = """
    CREATE TABLE test_customers (
    id integer PRIMARY KEY,
    first_name VARCHAR(255),
    last_name  VARCHAR(255),
    email  VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    block_id BIGINT,
    state_fips BIGINT,
    state_code VARCHAR(10),
    block_pop BIGINT);"""
    database_manager.send_sql(sql_query)



def set_postgresqlmanager_db_variables():
    """
    set_db_variables is used to provide the credentials to the integration postgresql database.
    :return:
    """
    dbvars = {"username": "testing1234",
              "password": "testing1234",
              "hostname": "127.0.0.1",
              "database": "testing1234",
              "table": "customers"}
    return dbvars
