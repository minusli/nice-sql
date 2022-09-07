from typing import List

import pymysql
import pymysql.cursors
from dbutils.pooled_db import PooledDB

from nicesql.sqlengine.base import SqlEngine
from nicesql.sqlresult import SqlResult


class Mysql(SqlEngine):
    def __init__(self, host: str = '127.0.0.1', port: int = 3306, dbname: str = None, user: str = None, password: str = None, maxconnections: int = None):
        self.pool = PooledDB(creator=pymysql, host=host, port=port, database=dbname, user=user, password=password,
                             maxconnections=maxconnections, blocking=True, setsession=['SET AUTOCOMMIT = 1'],
                             cursorclass=pymysql.cursors.DictCursor, charset='utf8mb4')

    def execute(self, sql: str, params: List) -> SqlResult:
        sql = sql.replace("?", "%s")
        with self.pool.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)

            rows = cursor.fetchall()
            rowcount = cursor.rowcount
            insertid = cursor.lastrowid

            return SqlResult(rows=rows, rowcount=rowcount, insertid=insertid)

    def close(self):
        self.pool.close()
