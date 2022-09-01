from typing import Type, List, Dict, Any, Optional, TypeVar

from nicesql.sqlmodel import SqlModel

M = TypeVar("M", SqlModel, Dict[str, Any])


class SqlResult:
    def __init__(self, rows: List[Dict[str, Any]], rowcount: int, insertid: str | int):
        self._rows = rows
        self._rowcount = rowcount
        self._insertid = insertid

    def all(self, model: Type[M] = None) -> List[M]:
        if not model:
            return self._rows
        return [model().fill(**row) for row in self._rows]

    def first(self, model: Type[M] = None) -> Optional[M]:
        if not self._rows:
            return None
        if not model:
            return self._rows[0]
        return model().fill(**self._rows[0])

    def rowcount(self):
        return self._rowcount

    def insertid(self):
        return self._insertid
