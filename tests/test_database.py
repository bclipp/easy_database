"""
This module is used to test the database module
"""

from unittest.mock import Mock

from database import database as db


def test_database_manager_send_sql():
    """
    This test is to verify the send_sql method works functionally without a database.
    """
    database_manager = db.DatabaseManager("this is a test string")
    database_manager.conn = Mock()
    # add methods needed
    database_manager.send_sql("this is sql")
    # verify called
