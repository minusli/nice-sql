from abc import ABCMeta, abstractmethod
from typing import List

from nicesql.sqlresult import SqlResult


class SqlEngine(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, sql: str, params: List) -> SqlResult:
        pass

    @abstractmethod
    def close(self):
        pass
