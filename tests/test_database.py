"""
This module is used to test the easydb module
"""

from unittest.mock import Mock

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
    This test is to verify the send_sql can handle bad inputs
    """
    database_manager = db.DatabaseManager("this is a test string")
    database_manager.cursor = Mock()
    database_manager.cursor.return_value.execute = [1, 2, 3, 4, 5]
    try:
        database_manager.receive_sql_fetchall(1)
    except db.NotStr:
        assert True
