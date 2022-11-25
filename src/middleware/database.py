import psycopg
from psycopg import connection, cursor


class PostgresDatabase:

    def __init__(self, host: str, database: str, user: str, password: str):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

        self.__connect()

    def __connect(self):
        self.__connection = psycopg.connect(user=self.user, password=self.password, host=self.host, port="5432", dbname=self.database)
        self.__connection.autocommit = True

        self.__cursor = self.__connection.cursor(row_factory=psycopg.rows.dict_row)

    def get_cursor(self) -> cursor:
        if not self.__cursor:
            self.__connect()

        return self.__cursor

    def get_connection(self) -> connection:
        if not self.__connection:
            self.__connect()

        return self.__connection

    def close_session(self):
        self.__cursor.close()
        self.__connection.close()
