from typing import Any

from nicesql.engine import Engine, Result
from nicesql.engine import add_db, register_engine
from nicesql.shortcut import insert, delete, update, select, sql as sql_


class DummyEngine(Engine):
    def __init__(self, **kwargs):
        pass

    def execute(self, nsql: str, params: Any) -> Result:
        # noinspection PyTypeChecker
        result = Result((nsql, params), (nsql, params), (nsql, params))
        return result


def setup_module():
    register_engine("dummy", DummyEngine)
    add_db("dummy:///dummy")


# noinspection DuplicatedCode, PyMethodMayBeStatic, PyShadowingBuiltins
class TestShortcuts:
    @insert("insert into dummy(a, b, c) values({a}, {b}, {c})")
    def self_insert(self, b, a, c=1):
        pass

    @classmethod
    @select("select * from dummy where a={a} AND b={b} OR c={c}")
    def cls_select(cls, a, **kwargs):
        pass

    @staticmethod
    @update("update dummy set a={a} where b in {b}")
    def sta_update(a, b=(1, 2, 3)):
        pass

    @sql_("create table() a={c}")
    def ddl(self, a=1, b=2, c=3):
        pass

    def test_insert(self):
        sql, params = self.self_insert(1, "2")
        assert sql == "insert into dummy(a, b, c) values(?, ?, ?)"
        assert params == ['2', 1, 1]

    def test_select(self):
        sql, params = self.cls_select(1, b="2", c=[1, "2"])
        assert sql == "select * from dummy where a=? AND b=? OR c=?,?"
        assert params == [1, '2', 1, '2']

    def test_update(self):
        sql, params = self.sta_update(1)
        assert sql == "update dummy set a=? where b in ?,?,?"
        assert params == [1, 1, 2, 3]

    def test_bind(self):
        sql, params = self.ddl().insertid()
        assert sql == "create table() a=?"
        assert params == [3]


# noinspection PyUnusedLocal
@delete("delete from dummy where a={a} and b like {b}")
def func_delete(a, b):
    pass


def test_delete():
    sql, params = func_delete(a=1, b="%2%")
    assert sql == "delete from dummy where a=? and b like ?"
    assert params == [1, "%2%"]
