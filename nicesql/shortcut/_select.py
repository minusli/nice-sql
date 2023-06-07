from typing import Optional, Type, List

from nicesql.db import Model, Row
from nicesql.shortcut._base import SQL


def select(nsql: str, **kwargs) -> "Select":
    return Select(nsql, **kwargs)


class Select(SQL):
    def __init__(self, nsql: str, **kwargs):
        super().__init__(nsql, **kwargs)

        self.__model: Optional[Type[Model]] = None
        self.__first: bool = False

    def execute(self, **kwargs) -> List[Row | Model] | Row | Model:
        result = super().execute(**kwargs)
        if self.__first:
            return result.first(self.__model)
        return result.all(self.__model)

    def model(self, model: Type[Model]) -> "Select":
        self.__model = model
        return self

    def first(self, model: Type[Model] = None) -> "Select":
        self.__first = True
        if model:
            self.__model = model
        return self
