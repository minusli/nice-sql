import sqlite3
import threading
from sqlite3 import Cursor
from typing import Any, List, Dict

from nicesql.sqlengine import SQLEngine
from nicesql.sqlresult import SqlResult


def row2dict_factory(cursor: Cursor, row: List[Any]) -> Dict[str, Any]:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Sqlite(SQLEngine):

    def __init__(self, db: str):
        self.conn = sqlite3.connect(db, isolation_level=None)
        self.conn.row_factory = row2dict_factory
        self.lock = threading.Lock()

    def execute(self, sql: str, params: List) -> SqlResult:
        with self.lock:
            cur = self.conn.cursor()
            cur.execute(sql, params)

            rows = cur.fetchall()
            rowcount = cur.rowcount
            insertid = cur.lastrowid

            cur.close()

            return SqlResult(rows=rows, rowcount=rowcount, insertid=insertid)

    def close(self):
        with self.lock:
            self.conn.close()
