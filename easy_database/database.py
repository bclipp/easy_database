"""
This modules holds Database manager related code
"""
from abc import ABC, abstractmethod

import psycopg2
import psycopg2.extras
import pandas as pd


class DatabaseManager(ABC):
    """
    Database is a abc or a interface for refering to all the database managers
    """

    @abstractmethod
    def open_conn(self):
        """
        creates the database conneciton
        :return:
        """

    @abstractmethod
    def close_conn(self):
        """
        closes the database conneciton
        :return:
        """

    @abstractmethod
    def receive_sql_fetchall(self, sql_query: str):
        """
        send sql and get a list of dict
        :param sql_query:
        :return:
        """

    @abstractmethod
    def send_sql(self, sql_query: str):
        """
        send SQL with not returned result
        :param sql_query:
        :return:
        """

    @abstractmethod
    def df_insert(self,
                  data_frame: pd.DataFrame,
                  table_name: str,
                  conflict_id: str = None):
        """
        used for taking a database and inserting it into a table
        :param data_frame:
        :param table_name:
        :param conflict_id:
        :return:
        """

    @abstractmethod
    def set_connection_data(self, set_connection_data: dict):
        """
        used for setting the conneciton string
        :param set_connection_data:
        :return:
        """


class PostgreSQLManger(DatabaseManager):
    """
    The PostgreSQLManger takes a connection string and will allow you to
    interact with the database in an abstract way.
    """

    def __init__(self):
        self.connection_string = None
        self.conn = None
        self.cursor = None
        self.connection_data = None

    def set_connection_data(self, set_connection_data: dict):
        """set's the connection data"""
        self.connection_data = set_connection_data

    def open_conn(self):
        """
        connect_db will setup a connection to the easydb
        """
        connection_data = self.connection_data
        database = connection_data["database"]
        username = connection_data["username"]
        db_ip_address = connection_data["db_ip_address"]
        password = connection_data["password"]
        try:
            conn = psycopg2.connect(dbname=database,
                                    user=username,
                                    host=db_ip_address,
                                    password=password,
                                    cursor_factory=psycopg2.extras.RealDictCursor)

        except psycopg2.DatabaseError as error:
            print()
            raise error
        self.cursor = conn.cursor()
        self.conn = conn
        self.conn.autocommit = True

    def close_conn(self):
        """
        close_conn will close the connection created with connect_db
        """
        self.cursor.close()

    def receive_sql_fetchall(self, sql_query: str) -> list:
        """
        receive_sql_fetchall takes a sql query and returns a
        list of dictionaries.
        :param sql_query: SQL statement
        :return: the output of the query
        """
        check_query(sql_query)
        try:
            self.cursor.execute(sql_query)
        except psycopg2.DatabaseError as error:
            self.conn.rollback()
            raise error
        return self.cursor.fetchall()

    def send_sql(self, sql_query: str):
        """
        send_sql is used when a result from the query is not needed.
        :param sql_query: SQL
        """
        check_query(sql_query)
        try:
            self.cursor.execute(sql_query)
        except psycopg2.DatabaseError as error:
            self.conn.rollback()
            raise error

    def df_insert(self,
                  data_frame: pd.DataFrame,
                  table_name: str,
                  conflict_id: str = None):
        """
        df_insert is used to insert data in a dataframe into a table in bulk
        :param data_frame: data to insert
        :param table_name: the table to update
        :param conflict_id:
        :return:
        """
        check_data_frame(data_frame)
        check_string(table_name)
        try:
            if not data_frame.empty:
                data_frame_columns = list(data_frame)
                columns = ",".join(data_frame_columns)
                values = "VALUES({})".format(
                    ",".join(["%s" for _ in data_frame_columns])
                )
                if conflict_id:
                    insert_query = "INSERT INTO {} ({}) {} ON CONFLICT ({}) DO NOTHING;" \
                        .format(table_name,
                                columns,
                                values,
                                conflict_id)
                else:
                    insert_query = "INSERT INTO {} ({}) {};" \
                        .format(table_name,
                                columns,
                                values)
                psycopg2.extras.execute_batch(
                    self.cursor, insert_query, data_frame.values
                )
        except psycopg2.DatabaseError as error:
            self.conn.rollback()
            raise error


class NotStr(Exception):
    """
    NotStr is used for a custom Exception
    """


class NotDataFrame(Exception):
    """
    NotDataFrame is used for a custom Exception
    """


def check_query(sql_query: str):
    """
    check_query is used to perform checks against the sql query
    :param sql_query: SQL statement.
    :return:
    """
    if not isinstance(sql_query, str):
        raise NotStr("Query must be a valid string")


def check_string(string: str):
    """
    check_string is used to perform checks against the sql query
    :param string: SQL statement.
    :return:
    """
    if not isinstance(string, str):
        raise NotStr("input must be a valid string")


def check_data_frame(data_frame: pd.DataFrame):
    """
     check_data_frame is used to perform checks against the dataframe provided
    :param data_frame:
    :return:
    """
    if not isinstance(data_frame, pd.DataFrame):
        raise NotDataFrame("Query must be a valid DataFrame")
