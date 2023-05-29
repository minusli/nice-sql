from typing import Any

import pymysql
import pymysql.cursors
from dbutils.pooled_db import PooledDB

from nicesql import utils
from nicesql.engine import sqlformat
from nicesql.engine.base import Engine, Result


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

    def execute(self, nsql: str, data: Any) -> Result:
        sql, params = sqlformat.parse_nsql(nsql)
        params = [utils.pick_value(data, p) for p in params]

        sql, params = sqlformat.expand_sql(sql, params)  # support list

        sql = sql.replace("?", "%s")  # 占位符替换
        with self.pool.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)

            rows = cursor.fetchall()
            rowcount = cursor.rowcount
            insertid = cursor.lastrowid

            return Result(rows=rows, rowcount=rowcount, insertid=insertid)
