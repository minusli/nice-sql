from typing import Any, List

from nicesql.db._driver import LiteConnection
from nicesql.db._register import get_db
from nicesql.db._result import Result
from nicesql.db._sqlconv import sql_paramify
from nicesql.utils import logger, tls

_TLS_KEY_OF_CONNECTION = "__{}_db_connection"


def execute(sql: str, db: str = "default", **kwargs) -> Result:
    sql, params = sql_paramify(sql, kwargs)
    logger.debug("SQL: {} => {}".format(sql, sql))

    conn: LiteConnection = tls.get(_TLS_KEY_OF_CONNECTION.format(db))
    if conn:
        return _execute(conn, sql, params)

    conn = get_db(db).connection()
    conn.begin()
    try:
        result = _execute(conn, sql, params)
        conn.commit()
        return result
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _execute(conn: LiteConnection, sql: str, params: List[Any]) -> Result:
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        rowcount = cursor.rowcount()
        insertid = cursor.lastrowid()

        return Result(rows=rows, rowcount=rowcount, insertid=insertid)
    finally:
        if cursor:
            cursor.close()


def transaction(db="default"):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            conn = tls.get(_TLS_KEY_OF_CONNECTION.format(db))
            if conn:
                return fn(*args, **kwargs)

            conn = get_db(db).connection()
            conn.begin()
            try:
                tls.put(_TLS_KEY_OF_CONNECTION.format(db), conn)
                r = fn(*args, **kwargs)
                conn.commit()
                return r
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()
                tls.pop(_TLS_KEY_OF_CONNECTION.format(db))

        return wrapper

    return decorator
