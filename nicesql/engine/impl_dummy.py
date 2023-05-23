from typing import List

from nicesql.engine.base import Engine, Result


class DummyEngine(Engine):
    def init(self, **kwargs):
        pass

    def execute(self, sql: str, params: List) -> Result:
        # noinspection PyTypeChecker
        result = Result((sql, params), (sql, params), (sql, params))
        return result
