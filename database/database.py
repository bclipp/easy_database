"""
This modules holds Database manager related code
"""
import pandas as pd
import psycopg2
import psycopg2.extras


class DatabaseManager:
    """
    The databaseManager takes a connection string and will allow you to
    interact with the database in an abstract way.
    """
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.conn = None
        self.cursor = None

    def connect_db(self):
        """
        connect_db will setup a connection to the database
        """
        connection_string = self.connection_string
        try:
            conn = psycopg2.connect(connection_string,
                                    cursor_factory=psycopg2.extras.RealDictCursor)

        except psycopg2.DatabaseError as error:
            self.conn.rollback()
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

    def update_df(self,
                  data_frame: pd.DataFrame,
                  sql_query: str):
        """
        update table row by row
        :param data_frame: data to insert
        :param sql_query: SQL statement
        :return:
        """
        for i in range(len(data_frame)):
            row = data_frame.iloc[i]
            self.send_sql(sql_query, row)
