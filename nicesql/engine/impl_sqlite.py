import sqlite3
import threading
from sqlite3 import Cursor
from typing import Any, List, Dict

from nicesql import utils
from nicesql.engine import sqlformat
from nicesql.engine.base import Engine, Result


class SqliteEngine(Engine):
    def __init__(self, **kwargs):
        database = kwargs.get('database')
        self.conn = sqlite3.connect(database, isolation_level=None, check_same_thread=False)
        self.conn.row_factory = _row2dict_factory
        if kwargs.get("debug", "").lower() == "true":
            self.conn.set_trace_callback(lambda sql: print(f"SQL: {sql}"))
        self.lock = threading.Lock()

    def execute(self, nsql: str, data: Any) -> Result:
        sql, params = sqlformat.parse_nsql(nsql)
        params = [utils.pick_value(data, p) for p in params]

        # support list
        sql, params = sqlformat.expand_sql(sql, params)

        with self.lock:
            cur = self.conn.cursor()
            cur.execute(sql, params)

            rows = cur.fetchall()
            rowcount = cur.rowcount
            insertid = cur.lastrowid

            cur.close()

            return Result(rows=rows, rowcount=rowcount, insertid=insertid)


def _row2dict_factory(cursor: Cursor, row: List[Any]) -> Dict[str, Any]:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
