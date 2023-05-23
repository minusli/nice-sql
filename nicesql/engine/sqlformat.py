import re
from typing import List, Any, Tuple


def parse_nsql(nsql: str) -> Tuple[str, List[Any]]:
    regex = r"{([^{}]+)}"
    placeholder = "?"

    params = []
    for g in re.findall(regex, nsql):
        params.append(re.sub(r"\s+", "", g))
    sql = re.sub(regex, placeholder, nsql)
    return sql, params


def expand_sql(sql: str, params: List[Any]) -> Tuple[str, List[Any]]:
    if not params:
        return sql, params

    param_cnt = 0
    q_cnt = 0
    param_index = len(params)
    q_index = len(sql)
    while 0 <= param_index:
        param_index -= 1
        param_cnt += 1

        param = params[param_index]
        if isinstance(param, (list, tuple)):
            if isinstance(param, (tuple,)):
                param = list(param)
            params = params[:param_index] + param + params[param_index + 1:]
            while q_cnt < param_cnt:
                q_index -= 1
                if sql[q_index] == "?":  # q_index 不可能越界
                    q_cnt += 1
            sql = sql[:q_index] + ",".join(['?'] * len(param)) + sql[q_index + 1:]

    return sql, params
