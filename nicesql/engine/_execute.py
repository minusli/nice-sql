from typing import Any

from nicesql.engine._register import get_db
from nicesql.engine._result import Result
from nicesql.sqlconv import sql_paramify


def execute(nsql: str, data: Any = None, db: str = "default") -> Result:
    sql, params = sql_paramify(nsql, data)
    return get_db(db).execute(sql, params)
