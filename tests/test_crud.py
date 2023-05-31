from typing import List

import pytest

from nicesql.engine import add_db, remove_db
from nicesql.shortcut import insert, delete, update, select, ddl


class Person:
    def __init__(self):
        self.id = None
        self.name = None


dbs = [
    "mysql://localhost/test?user=test&password=test",
    "sqlite:///:memory:?debug=true"
]


@pytest.fixture
def db(request):
    url = request.param
    add_db(url)
    if url.startswith("mysql:"):
        ddl("""
            create table if not exists person(
                id      int not null primary key auto_increment,
                name    varchar(127)
            )
        """).execute()
    elif url.startswith("sqlite:"):
        ddl("""
            create table if not exists person(
                id      integer not null primary key autoincrement,
                name    text
            )
        """).execute()
    else:
        raise Exception("unknown db url")
    yield url
    ddl("drop table if exists person").execute()
    remove_db()


# noinspection DuplicatedCode, PyMethodMayBeStatic, PyShadowingBuiltins
class Dao:
    @classmethod
    @insert("insert into person(name) values({name})")
    def insert(cls, name: str) -> int:
        pass

    @classmethod
    @delete("delete from person where id={id}")
    def delete(cls, id: int) -> int:
        pass

    @classmethod
    @update("update person set name={name} where id={id}")
    def update(cls, id: int, name: str) -> int:
        pass

    @classmethod
    @select("select * from person where id={ id }").first(Person)
    def get(cls, id: int) -> Person:
        pass

    @classmethod
    @select("select * from person where id in ({ ids })").model(Person)
    def gets(cls, *ids: int) -> List[Person]:
        pass

    @classmethod
    @select("select * from person where name like { name }").model(Person)
    def find(cls, name: str) -> List[Person]:
        pass


@pytest.mark.parametrize("db", dbs, indirect=True)
def test_insert(db):
    name1 = "insert001"
    name2 = "insert002"
    name3 = "insert003"
    new_id1 = Dao.insert(name1)
    new_id2 = Dao.insert(name2)
    new_id3 = Dao.insert(name3)

    person1 = Dao.get(new_id1)
    person2 = Dao.get(new_id2)
    person3 = Dao.get(new_id3)
    assert person1
    assert person2
    assert person3
    assert person1.name == name1
    assert person2.name == name2
    assert person3.name == name3


@pytest.mark.parametrize("db", dbs, indirect=True)
def test_delete(db):
    name = "delete001"
    new_id = Dao.insert(name)
    assert Dao.delete(new_id) == 1
    assert Dao.delete(new_id) == 0

    person = Dao.get(new_id)
    assert person is None


@pytest.mark.parametrize("db", dbs, indirect=True)
def test_update(db):
    name = "update001"
    update_name = "update001_new"
    new_id = Dao.insert(name)
    assert Dao.update(new_id, update_name) == 1
    person = Dao.get(new_id)
    assert person
    assert person.name == update_name


@pytest.mark.parametrize("db", dbs, indirect=True)
def test_select(db):
    name1 = "gets001"
    name2 = "gets002"
    id1 = Dao.insert(name1)
    id2 = Dao.insert(name2)
    person1 = Dao.get(id1)
    person2 = Dao.get(id2)
    persons = Dao.gets(id1, id2)
    persons_by_find = Dao.find("gets%")
    assert person1.name == name1
    assert person2.name == name2
    assert set([p.id for p in persons]) == {id1, id2}
    assert set([p.name for p in persons]) == {name1, name2}
    assert set([p.id for p in persons_by_find]) == {id1, id2}
    assert set([p.name for p in persons_by_find]) == {name1, name2}
