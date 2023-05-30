from typing import List

from nicesql.engine import add_db
from nicesql.shortcut import insert, delete, update, select, ddl


class Person:
    def __init__(self):
        self.id = None
        self.name = None


def setup_module():
    add_db(sqlite="sqlite:///:memory:?debug=true")
    create_table()


def teardown_module():
    drop_table()


@ddl("""
create table if not exists person(
    id      integer not null primary key,
    name    varchar(127)
)
""").db("sqlite")
def create_table():
    pass


@ddl("drop table if exists person").db('sqlite')
def drop_table():
    pass


# noinspection DuplicatedCode, PyMethodMayBeStatic, PyShadowingBuiltins
class TestSqlite:
    @insert("insert into person(name) values({name})").db('sqlite')
    def insert(self, name: str) -> int | str:
        pass

    @delete("delete from person where id={id}").db('sqlite')
    def delete(self, id: int) -> int:
        pass

    @update("update person set name={name} where id={id}").db('sqlite')
    def update(self, id: int, name: str) -> int:
        pass

    @select("select * from person where id={ id }").db('sqlite').first(Person)
    def get(self, id: int) -> Person:
        pass

    @select("select * from person where id in ({ ids })").db('sqlite').model(Person)
    def gets(self, *ids: int) -> List[Person]:
        pass

    @select("select * from person where name like { name }").db('sqlite').model(Person)
    def find(self, name: str) -> List[Person]:
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

    def test_gets(self):
        name1 = "gets001"
        name2 = "gets002"
        id1 = self.insert(name1)
        id2 = self.insert(name2)
        persons = self.gets(id1, id2)
        assert len(persons) == 2
        assert persons[0].id == id1
        assert persons[1].id == id2
        assert persons[0].name == name1
        assert persons[1].name == name2
