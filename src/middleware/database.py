import time
import psycopg
from psycopg import connection, cursor
from psycopg import OperationalError
from loguru import logger


class PostgresDatabase:

    def __init__(self, host: str, database: str, user: str, password: str):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection_retries = 3

        self.__connect()

    def __connect(self):
        try:
            self.__connection = psycopg.connect(user=self.user, password=self.password, host=self.host, port="5432", dbname=self.database)
            self.__connection.autocommit = True
        except OperationalError as e:
            # a workaround for docker compose not building postgres contains first

            logger.warning("Database is not ready.. retrying in one second. Retries left: {}".format(self.connection_retries))
            self.connection_retries -= 1

            if self.connection_retries < 0:
                raise e

            time.sleep(1)
            self.__connect()

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
