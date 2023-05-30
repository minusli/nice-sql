import sqlite3
import threading
from abc import ABCMeta, abstractmethod
from sqlite3 import Cursor
from typing import Any, List, Dict

import pymysql
import pymysql.cursors
from dbutils.pooled_db import PooledDB

from nicesql.engine._result import Result


class Engine(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, sql: str, params: List[Any]) -> Result:
        pass


class MysqlEngine(Engine):
    def __init__(self, **kwargs):
        host = kwargs['host']
        port = kwargs.get('port') or 3306
        database = kwargs.get('database')
        user = kwargs.get("user")
        password = kwargs.get("password")
        maxconnections = kwargs.get("maxconnections")
        charset = kwargs.get("charset", "utf8mb4")

        self.pool = PooledDB(creator=pymysql, host=host, port=port, database=database, user=user, password=password,
                             maxconnections=maxconnections, blocking=True, setsession=['SET AUTOCOMMIT = 1'],
                             cursorclass=pymysql.cursors.DictCursor, charset=charset)

    def execute(self, sql: str, params: List[Any]) -> Result:
        sql = sql.replace("?", "%s")  # 占位符替换
        with self.pool.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)

            rows = cursor.fetchall()
            rowcount = cursor.rowcount
            insertid = cursor.lastrowid

            return Result(rows=rows, rowcount=rowcount, insertid=insertid)


class SqliteEngine(Engine):
    def __init__(self, **kwargs):
        database = kwargs.get('database')
        self.conn = sqlite3.connect(database, isolation_level=None, check_same_thread=False)
        self.conn.row_factory = _sqlite3_row2dict_factory
        if kwargs.get("debug", "").lower() == "true":
            self.conn.set_trace_callback(lambda sql: print(f"SQL: {sql}"))
        self.lock = threading.Lock()

    def execute(self, sql: str, params: List[Any]) -> Result:
        with self.lock:
            cur = self.conn.cursor()
            cur.execute(sql, params)

            rows = cur.fetchall()
            rowcount = cur.rowcount
            insertid = cur.lastrowid

            cur.close()

            return Result(rows=rows, rowcount=rowcount, insertid=insertid)


def _sqlite3_row2dict_factory(cursor: Cursor, row: List[Any]) -> Dict[str, Any]:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
