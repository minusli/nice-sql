from typing import List

import nicesql
from nicesql.sqlengine.base import SqlEngine
from nicesql.sqlresult import SqlResult


class Dummy(SqlEngine):
    def execute(self, sql: str, params: List) -> SqlResult:
        # noinspection PyTypeChecker
        result = SqlResult((sql, params), (sql, params), (sql, params))
        return result

    def close(self):
        pass


def setup_module():
    nicesql.register(Dummy())


def teardown_module():
    nicesql.close()


# noinspection DuplicatedCode, PyMethodMayBeStatic, PyShadowingBuiltins
class TestShortcuts:
    @nicesql.insert("insert into dummy(a, b, c) values({a}, {b}, {c})")
    def self_insert(self, b, a, c=1):
        pass

    @classmethod
    @nicesql.select("select * from dummy where a={a} AND b={b} OR c={c}")
    def cls_select(cls, a, **kwargs):
        pass

    @staticmethod
    @nicesql.update("update dummy set a={a} where b in {b}")
    def sta_update(a, b=(1, 2, 3)):
        pass

    @nicesql.bind("create table() a={c}")
    def bind(self, a=1, b=2, c=3):
        pass

    def test_insert(self):
        sql, params = self.self_insert(1, "2")
        assert sql == "insert into dummy(a, b, c) values(?, ?, ?)"
        assert params == ["2", 1, 1]

    def test_select(self):
        sql, params = self.cls_select(1, b="2", c=[1, "2"])
        assert sql == "select * from dummy where a=? AND b=? OR c=?"
        assert params == [1, "2", [1, "2"]]

    def test_update(self):
        sql, params = self.sta_update(1)
        assert sql == "update dummy set a=? where b in ?"
        assert params == [1, (1, 2, 3)]

    def test_bind(self):
        sql, params = self.bind().insertid()
        assert sql == "create table() a=?"
        assert params == [3]


# noinspection PyUnusedLocal
@nicesql.delete("delete from dummy where a={a} and b like {b}")
def func_delete(a, b):
    pass


def test_delete():
    sql, params = func_delete(a=1, b="%2%")
    assert sql == "delete from dummy where a=? and b like ?"
    assert params == [1, "%2%"]
