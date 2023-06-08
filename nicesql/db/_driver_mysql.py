from typing import List, Dict, Any

import pymysql
from dbutils.pooled_db import PooledDB, PooledSharedDBConnection, PooledDedicatedDBConnection
from pymysql.cursors import Cursor, DictCursor

from nicesql.db._driver import LiteDriver, LiteConnection, LiteCursor


class Mysql(LiteDriver):
    def __init__(self, hostname: str, port: int, username: str, password: str, database: str, **kwargs):
        super().__init__(hostname, port, username, password, database, **kwargs)

        autocommit = self.get_autocommit()
        charset = self.get_charset()

        self.pool = PooledDB(creator=pymysql, host=self.hostname, port=self.port, database=self.database, user=self.username, password=self.password,
                             blocking=True, cursorclass=DictCursor, charset=charset, autocommit=autocommit)

    def connection(self) -> "LiteConnection":
        return MysqlConnection(self.pool.connection())

    def get_autocommit(self) -> bool:
        return str(self.kwargs.get("autocommit", "")).lower() in ("true", "1")

    def get_charset(self) -> str:
        return str(self.kwargs.get("charset", ""))


class MysqlConnection(LiteConnection):
    def __init__(self, connection: PooledSharedDBConnection | PooledDedicatedDBConnection):
        self.connection = connection

    def begin(self):
        self.connection.begin()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cursor(self) -> "LiteCursor":
        return MysqlCursor(self.connection.cursor())

    def close(self):
        self.connection.close()


class MysqlCursor(LiteCursor):
    def __init__(self, cursor: Cursor):
        self.cursor = cursor

    def execute(self, sql: str, params: List[Any]):
        sql = sql.replace("?", "%s")
        self.cursor.execute(sql, params)

    def lastrowid(self) -> int | str:
        return self.cursor.lastrowid

    def rowcount(self) -> int:
        return self.cursor.rowcount

    def fetchall(self) -> List[Dict[str, Any]]:
        # noinspection PyTypeChecker
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
