"""
This module is used to test the easydb module
"""

from unittest.mock import Mock
from unittest.mock import patch

import pandas as pd

import easydb.database as db


def test_send_sql_string():
    """
    This test is to verify the send_sql method works functionally without a easydb.
    """
    database_manager = db.DatabaseManager("this is a test string")
    database_manager.cursor = Mock()
    database_manager.cursor.return_value.execute = [1, 2, 3, 4, 5]
    database_manager.send_sql("this is sql")
    assert database_manager.cursor.execute.call_count == 1


def test_send_sql_not_string():
    """
    This test is to verify the send_sql can handle bad inputs
    """
    database_manager = db.DatabaseManager("this is a test string")
    database_manager.cursor = Mock()
    database_manager.cursor.return_value.execute = [1, 2, 3, 4, 5]
    try:
        database_manager.send_sql(1)
    except db.NotStr:
        assert True


def test_receive_sql_fetchall():
    """
        This test is to verify the test_receive_sql_fetchall
        method works functionally without a easydb.
    """
    database_manager = db.DatabaseManager("this is a test string")
    database_manager.cursor = Mock()
    database_manager.cursor.return_value.execute = [1, 2, 3, 4, 5]
    database_manager.receive_sql_fetchall("this is sql")
    assert database_manager.cursor.execute.call_count == 1


def test_receive_sql_fetchall_not_string():
    """
    This test is to verify the test_receive_sql_fetchall can handle bad inputs
    """
    database_manager = db.DatabaseManager("this is a test string")
    database_manager.cursor = Mock()
    database_manager.cursor.return_value.execute = [1, 2, 3, 4, 5]
    try:
        database_manager.receive_sql_fetchall(1)
    except db.NotStr:
        assert True


@patch("easydb.database.psycopg2.extras.execute_batch")
def test_df_insert(mock_execute_batch):
    """
        This test is to verify the df_insert
        method works functionally without a easydb.
    """
    database_manager = db.DatabaseManager("this is a test string")
    database_manager.cursor = Mock()
    database_manager.cursor.return_value.execute = [1, 2, 3, 4, 5]
    data_frame = pd.DataFrame({'Brand': ['Honda Civic', 'Toyota Corolla', 'Ford Focus', 'Audi A4'],
                               'Price': [22000, 25000, 27000, 35000]
                               }, columns=['Brand', 'Price'])
    database_manager.df_insert(data_frame, "fake_table")
    assert mock_execute_batch.call_count == 1


def test_df_insert_not_df():
    """
    This test is to verify the df_insert can handle bad inputs
    """
    database_manager = db.DatabaseManager("this is also a test string")
    database_manager.cursor = Mock()
    database_manager.cursor.return_value.execute = [1, 2, 3, 4, 5]
    data_frame = "I am not a dataframe"
    try:
        database_manager.df_insert(data_frame, "fake_table")
    except db.NotDataFrame:
        assert True


def test_df_insert_table_not_string():
    """
    This test is to verify the df_insert can handle bad input for table
    """
    database_manager = db.DatabaseManager("this is also a test string")
    database_manager.cursor = Mock()
    database_manager.cursor.return_value.execute = [1, 2, 3, 4, 5]
    data_frame = pd.DataFrame({'Brand': ['Honda Civic', 'Toyota Corolla', 'Ford Focus', 'Audi A4'],
                               'Price': [22000, 25000, 27000, 35000]
                               }, columns=['Brand', 'Price'])
    try:
        database_manager.df_insert(data_frame, 2)
    except db.NotStr:
        assert True
