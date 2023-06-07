import re
from typing import Any, Tuple, List

import datapath


def sql_paramify(nsql: str, data: Any) -> Tuple[str, List[Any]]:
    sql, params = __extract_and_replace_placeholder(nsql)
    values = [datapath.value(data, p) for p in params]
    sql, values = __expand_list(sql, values)
    return sql, values


def __extract_and_replace_placeholder(nsql: str) -> Tuple[str, List[str]]:
    regex = r"{([^{}]+)}"
    placeholder = "?"

    params = []
    for g in re.findall(regex, nsql):
        params.append(g.strip())
    sql = re.sub(regex, placeholder, nsql)
    return sql, params


def __expand_list(sql: str, values: List[Any]) -> Tuple[str, List[Any]]:
    if not values:
        return sql, values

    value_cnt = 0
    q_cnt = 0
    value_index = len(values)
    q_index = len(sql)
    while 0 <= value_index:
        value_index -= 1
        value_cnt += 1

        v = values[value_index]
        if isinstance(v, (list, tuple)):
            if isinstance(v, (tuple,)):
                v = list(v)
            values = values[:value_index] + v + values[value_index + 1:]
            while q_cnt < value_cnt:
                q_index -= 1
                if sql[q_index] == "?":  # q_index 不可能越界
                    q_cnt += 1
            sql = sql[:q_index] + ",".join(['?'] * len(v)) + sql[q_index + 1:]

    return sql, values
