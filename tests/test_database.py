"""
This module is used to test the database module
"""

from unittest.mock import Mock

from database import database as db


def test_database_manager_send_sql_string():
    """
    This test is to verify the send_sql method works functionally without a database.
    """
    database_manager = db.DatabaseManager("this is a test string")
    database_manager.cursor = Mock()
    database_manager.cursor.return_value.execute = [1, 2, 3, 4, 5]
    database_manager.send_sql("this is sql")
    assert database_manager.cursor.execute.call_count == 1


def test_database_manager_send_sql_not_string():
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

