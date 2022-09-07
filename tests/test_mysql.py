import nicesql
from nicesql.sqlengine.mysql import Mysql
from nicesql.sqlmodel import SqlModel


class Person(SqlModel):
    def __init__(self):
        self.id = None
        self.name = None


# noinspection DuplicatedCode, PyMethodMayBeStatic, PyShadowingBuiltins
class TestMysql:
    def setup(self):
        nicesql.register(Mysql(dbname="test", user="test", password="test"))
        nicesql.execute("""
            create table if not exists person(
                id      int not null primary key auto_increment,
                name    varchar(127)
            )
        """)

    def teardown(self):
        nicesql.execute("""
            drop table if exists person
        """)
        nicesql.close()

    @nicesql.insert("insert into person(name) values({name})")
    def insert(self, name: str) -> int:
        pass

    @nicesql.select("select * from person where id={ id }", model=Person, first=True)
    def get(self, id: int) -> Person:
        pass

    @nicesql.update("update person set name={name} where id={id}")
    def update(self, id: int, name: str) -> int:
        pass

    @nicesql.delete("delete from person where id={id}")
    def delete(self, id: int) -> int:
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
        person = self.get(new_id)
        assert person
        assert person.name == name

        assert self.delete(new_id) == 1
        person = self.get(new_id)
        assert person is None

    def test_update(self):
        name = "update001"
        update_name = "update002"
        new_id = self.insert(name)
        person = self.get(new_id)
        assert person
        assert person.name == name
        assert self.update(new_id, update_name) == 1
        person = self.get(new_id)
        assert person
        assert person.name == update_name
