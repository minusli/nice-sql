import sqlite3
import threading
from sqlite3 import Connection, Cursor
from typing import List, Dict, Any

from nicesql.db._driver import LiteDriver, LiteConnection, LiteCursor


class Sqlite(LiteDriver):
    def __init__(self, hostname: str, port: int, username: str, password: str, database: str, **kwargs):
        super().__init__(hostname, port, username, password, database, **kwargs)

        self.isolation_level = None if self.is_mem() else ""
        self.check_same_thread = False if self.is_mem() else True
        self.conn = None
        self.db_lock = None
        if self.is_mem():
            self.conn = sqlite3.connect(self.database, check_same_thread=self.check_same_thread, isolation_level=self.isolation_level)
            self.db_lock = threading.Lock()

    def connection(self) -> "LiteConnection":
        if self.is_mem():
            conn = self.conn
        else:
            conn = sqlite3.connect(self.database, check_same_thread=self.check_same_thread, isolation_level=self.isolation_level)
        conn.row_factory = _sqlite3_row2dict_factory

        return SqliteConnection(conn, self.is_mem(), self.db_lock)

    def is_mem(self):
        return self.database == ":memory:"


class SqliteConnection(LiteConnection):
    def __init__(self, connection: Connection, is_singleton: bool, db_lock: threading.Lock):
        self.connection = connection
        self.is_singleton = is_singleton
        self.db_lock = db_lock
        if self.is_singleton:
            self.db_lock.acquire()

    def begin(self):
        self.connection.execute("begin")

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cursor(self) -> "LiteCursor":
        return SqliteCursor(self.connection.cursor())

    def close(self):
        if self.is_singleton:
            self.db_lock.release()
            return

        self.connection.close()


class SqliteCursor(LiteCursor):
    def __init__(self, cursor: Cursor):
        self.cursor = cursor

    def execute(self, sql: str, params: List[Any]):
        self.cursor.execute(sql, params)

    def lastrowid(self) -> int | str:
        return self.cursor.lastrowid

    def rowcount(self) -> int:
        return self.cursor.rowcount

    def fetchall(self) -> List[Dict[str, Any]]:
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()


def _sqlite3_row2dict_factory(cursor: Cursor, row: List[Any]) -> Dict[str, Any]:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
