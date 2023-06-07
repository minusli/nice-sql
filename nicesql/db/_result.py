import inspect
from typing import Type, List, Dict, Any, TypeVar

Model = TypeVar("Model")
Row = Dict[str, Any]


class Result:
    def __init__(self, rows: List[Row], rowcount: int, insertid: Any):
        self._rows = rows
        self._rowcount = rowcount
        self._insertid = insertid

    def all(self, model: Type[Model] = None) -> List[Row | Model]:
        if not model:
            return self._rows
        return [fill_model(model(), **row) for row in self._rows]

    def first(self, model: Type[Model] = None) -> Row | Model:
        if not self._rows:
            return None
        if not model:
            return self._rows[0]
        return fill_model(model(), **self._rows[0])

    def rowcount(self) -> int:
        return self._rowcount

    def insertid(self) -> Any:
        return self._insertid


def fill_model(model: Model, **kwargs) -> Model:
    for k, v in kwargs.items():
        if not hasattr(model, k):
            continue

        origin_v = getattr(model, k, None)
        if origin_v and inspect.ismethod(origin_v):
            continue

        setattr(model, k, v)

    return model
