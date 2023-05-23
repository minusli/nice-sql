import nicesql
from nicesql.engine import reg_engine
from nicesql.shortcut.annotate import insert, delete, update, select, ddl


class Person:
    def __init__(self):
        self.id = None
        self.name = None


# noinspection DuplicatedCode, PyMethodMayBeStatic, PyShadowingBuiltins
class TestSqlite:
    def setup(self):
        reg_engine("sqlite:///:memory:/")
        self.create_table()

    @ddl("""
    create table if not exists person(
        id      integer not null primary key,
        name    varchar(127)
    )
    """)
    def create_table(self):
        pass

    @insert("insert into person(name) values({name})")
    def insert(self, name: str) -> int:
        pass

    @delete("delete from person where id={id}")
    def delete(self, id: int) -> int:
        pass

    @update("update person set name={name} where id={id}")
    def update(self, id: int, name: str) -> int:
        pass

    @select("select * from person where id={ id }", model=Person, first=True)
    def get(self, id: int) -> Person:
        pass

    @select("select * from person where id in { ids }", model=Person)
    def gets(self, *ids: int) -> Person:
        pass

    @select("select * from person where name like { name }", model=Person)
    def find(self, name: str) -> Person:
        pass

    def test_insert(self):
        name = "insert001"
        new_id = self.insert(name)

        person = self.get(new_id)
        assert person
        assert person.name == name

    def test_delete(self):
        name = "delete001"
        new_id = self.insert(name)
        assert self.delete(new_id) == 1

        person = self.get(new_id)
        assert person is None

    def test_update(self):
        name = "update001"
        update_name = "update002"
        new_id = self.insert(name)
        assert self.update(new_id, update_name) == 1
        person = self.get(new_id)
        assert person
        assert person.name == update_name
