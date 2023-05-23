# nicesql User Guide

------

### Talk is cheap. Show me the code

```python
"""
sqlite example

 --------------------
丨     person        丨
 --------------------
丨 id        int     丨
丨 name      string  丨
 --------------------
"""

from typing import List

from nicesql.engine import reg_engine
from nicesql.shortcut.annotate import insert, delete, update, select, ddl


class Person:
    def __init__(self):
        self.id = None
        self.name = None


def setup_module():
    reg_engine("mysql://localhost/test?user=test&password=test", alias="mysql")
    create_table()


def teardown_module():
    drop_table()


@ddl("""
create table if not exists person(
    id      integer not null primary key AUTO_INCREMENT,
    name    varchar(127)
)
""", engine="mysql")
def create_table():
    pass


@ddl("drop table if exists person", engine="mysql")
def drop_table():
    pass


# noinspection DuplicatedCode, PyMethodMayBeStatic, PyShadowingBuiltins
class TestMysql:
    @insert("insert into person(name) values({name})", engine="mysql")
    def insert(self, name: str) -> int | str:
        pass

    @delete("delete from person where id={id}", engine="mysql")
    def delete(self, id: int) -> int:
        pass

    @update("update person set name={name} where id={id}", engine="mysql")
    def update(self, id: int, name: str) -> int:
        pass

    @select("select * from person where id={ id }", model=Person, first=True, engine="mysql")
    def get(self, id: int) -> Person:
        pass

    @select("select * from person where id in ({ ids })", model=Person, engine="mysql")
    def gets(self, *ids: int) -> List[Person]:
        pass

    @select("select * from person where name like { name }", model=Person, engine="mysql")
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
```
