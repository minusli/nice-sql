from typing import Callable

from nicesql.db import execute, Result
from nicesql.shortcut._utils import extract_valid_params


def sql(nsql: str, **kwargs) -> "SQL":
    return SQL(nsql, **kwargs)


class SQL:
    def __init__(self, nsql: str, **kwargs):
        self.__nsql: str = nsql
        self.__kwargs = kwargs
        self.__db: str = "default"

    def execute(self, **kwargs) -> Result:
        kwargs = {}
        kwargs.update(self.__kwargs)
        kwargs.update(kwargs)
        return execute(self.__nsql, db=self.__db, **kwargs)

    def __call__(self, fn: Callable) -> Callable:
        def wrap(*args, **kwargs):
            kwargs = extract_valid_params(fn, *args, **kwargs)
            return self.execute(**kwargs)

        return wrap

    def db(self, db="default") -> "SQL":
        self.__db = db
        return self
