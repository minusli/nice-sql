import json
from typing import Any

import math


def pick_value(data: Any, key: str) -> Any:
    """
    支持递归查找，支持管道处理
    """
    if not key:
        return data

    pipes = key.split("|")
    keys = pipes[0].split(".")
    pipes = pipes[1:]

    value = data
    for k in keys:
        k = k.strip()
        value = __getvalue(value, k)

    for pipe in pipes:
        pipe = pipe.strip()
        params = pipe.split(" ")
        value = __exec_pipe(params[0], value, *params[1:])

    return value


def __getvalue(data: Any, key: str) -> Any:
    if isinstance(data, dict):
        return data[key]

    if isinstance(data, (list, tuple, set)):
        return [__getvalue(item, key) for item in data]

    return getattr(data, key)


def __exec_pipe(pipe_name: str, value: Any, *args: str) -> Any:
    return __pipes[pipe_name](value, *args)


__pipes = {
    "str": lambda v: str(v),
    "jsondump": lambda v: json.dumps(v),
    "jsonload": lambda v: json.loads(v),
    "%": lambda v, prec=None: __pipe_percent(v, prec),
    "int": lambda v: int(v),
    "float": lambda v: float(v),
    "ceil": lambda v: math.ceil(v),
    "floor": lambda v: math.floor(v),
    "round": lambda v, prec=None: __pipe_round(v, prec),
}


def __pipe_percent(v: Any, prec=None):
    v = "{}".format(v * 100)

    if prec:
        prec = int(prec)
        cur_prec = 0
        i = v.find(".")
        if i >= 0:
            cur_prec = len(v) - i - 1
        if cur_prec < prec:
            if cur_prec == 0:
                v += "."
            v += "0" * (prec - cur_prec)
        if cur_prec > prec:
            v = v[:prec - cur_prec]
            v = v.strip(".")
    else:
        if "." in v:
            while v[-1] == "0":
                v = v[:-1]
            v = v.strip(".")

    return v + "%"


def __pipe_round(v: Any, prec=None):
    if prec:
        prec = int(prec)
    else:
        prec = 0

    return round(v, prec)
