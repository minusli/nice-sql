from typing import Any

from nicesql.shortcut._base import SQL


def insert(nsql: str, **kwargs) -> "Insert":
    return Insert(nsql, **kwargs)


class Insert(SQL):
    def __init__(self, nsql: str, **kwargs):
        super().__init__(nsql, **kwargs)

    def execute(self, **kwargs) -> Any:
        result = super().execute(**kwargs)
        return result.insertid()
