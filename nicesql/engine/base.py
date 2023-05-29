from abc import ABCMeta, abstractmethod
from typing import Type, List, Dict, Any

from nicesql.utils import fill_model


class Engine(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, nsql: str, data: Any) -> "Result":
        pass


class Result:
    def __init__(self, rows: List[Dict[str, Any]], rowcount: int, insertid: Any):
        self._rows = rows
        self._rowcount = rowcount
        self._insertid = insertid

    def all(self, model: Type = None) -> List[Any]:
        if not model:
            return self._rows
        return [fill_model(model(), **row) for row in self._rows]

    def first(self, model: Type = None) -> Any:
        if not self._rows:
            return None
        if not model:
            return self._rows[0]
        return fill_model(model(), **self._rows[0])

    def rowcount(self) -> int:
        return self._rowcount

    def insertid(self) -> Any:
        return self._insertid
