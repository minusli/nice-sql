import re
from typing import Any, List, Tuple


def parsesql(nsql: str) -> Tuple[str, List[str]]:
    regex = r"{([^{}]+)}"
    params = []
    for g in re.findall(regex, nsql):
        params.append(re.sub(r"\s+", "", g))
    sql = re.sub(regex, "?", nsql)
    return sql, params


def getvalue(obj, key: str) -> Any:
    if not key:
        return obj
    if isinstance(obj, (list, tuple)):
        return [getvalue(o, key) for o in obj]

    keys = key.split(".", 1)
    k = keys[0].strip()
    nextk = keys[1].strip() if len(keys) == 2 else None

    if isinstance(obj, dict):
        return getvalue(obj[k], nextk)
    else:
        return getvalue(getattr(obj, k), nextk)
