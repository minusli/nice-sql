import nicesql
from nicesql import Sqlite, SqlModel


class Person(SqlModel):
    def __init__(self):
        self.id = None
        self.name = None


# noinspection DuplicatedCode
class TestCRUDWithSelf:
    # noinspection PyMethodMayBeStatic
    def setup(self):
        nicesql.register(Sqlite(":memory:"))
        nicesql.execute("""
            create table if not exists person(
                id      integer not null primary key,
                name    varchar(127)
            )
        """)

    # noinspection PyMethodMayBeStatic
    def teardown(self):
        nicesql.close()

    @nicesql.insert("insert into person(name) values({name})")
    def insert(self, name: str) -> int:
        pass

    # noinspection PyShadowingBuiltins
    @nicesql.select("select * from person where id={ id }", model=Person, first=True)
    def get(self, id: int) -> Person:
        pass

    # noinspection PyShadowingBuiltins
    @nicesql.update("update person set name={name} where id={id}")
    def update(self, id: int, name: str) -> int:
        pass

    # noinspection PyShadowingBuiltins
    @nicesql.delete("delete from person where id={id}")
    def delete(self, id: int) -> int:
        pass

    # noinspection PyShadowingBuiltins
    @nicesql.delete("delete from person where id={id}")
    def delete_0(self, id: int = 0) -> int:
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
        assert self.delete_0() == 0

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


# noinspection DuplicatedCode
class TestCRUDWithCls:
    # noinspection PyMethodMayBeStatic
    def setup(self):
        nicesql.register(Sqlite(":memory:"))
        nicesql.execute("""
                create table if not exists person(
                    id      integer not null primary key,
                    name    varchar(127)
                )
            """)

    # noinspection PyMethodMayBeStatic
    def teardown(self):
        nicesql.close()

    @classmethod
    @nicesql.insert("insert into person(name) values({name})")
    def insert(cls, name: str) -> int:
        pass

    # noinspection PyShadowingBuiltins
    @classmethod
    @nicesql.select("select * from person where id={ id }", model=Person, first=True)
    def get(cls, id: int) -> Person:
        pass

    # noinspection PyShadowingBuiltins
    @classmethod
    @nicesql.update("update person set name={name} where id={id}")
    def update(cls, id: int, name: str) -> int:
        pass

    # noinspection PyShadowingBuiltins
    @classmethod
    @nicesql.delete("delete from person where id={id}")
    def delete(cls, id: int) -> int:
        pass

    def test_insert(self):
        name = "insert001"
        new_id = TestCRUDWithCls.insert(name)

        person = TestCRUDWithCls.get(new_id)
        assert person
        assert person.name == name

    def test_delete(self):
        name = "delete001"
        new_id = TestCRUDWithCls.insert(name)
        person = TestCRUDWithCls.get(new_id)
        assert person
        assert person.name == name
        assert TestCRUDWithCls.delete(new_id) == 1
        person = TestCRUDWithCls.get(new_id)
        assert person is None

    def test_update(self):
        name = "update001"
        update_name = "update002"
        new_id = TestCRUDWithCls.insert(name)
        person = TestCRUDWithCls.get(new_id)
        assert person
        assert person.name == name
        assert TestCRUDWithCls.update(new_id, update_name) == 1
        person = TestCRUDWithCls.get(new_id)
        assert person
        assert person.name == update_name


# noinspection DuplicatedCode
class TestCRUDWithSta:
    # noinspection PyMethodMayBeStatic
    def setup(self):
        nicesql.register(Sqlite(":memory:"))
        nicesql.execute("""
                create table if not exists person(
                    id      integer not null primary key,
                    name    varchar(127)
                )
            """)

    # noinspection PyMethodMayBeStatic
    def teardown(self):
        nicesql.close()

    @staticmethod
    @nicesql.insert("insert into person(name) values({name})")
    def insert(name: str) -> int:
        pass

    # noinspection PyShadowingBuiltins
    @staticmethod
    @nicesql.select("select * from person where id={ id }", model=Person, first=True)
    def get(id: int) -> Person:
        pass

    # noinspection PyShadowingBuiltins
    @staticmethod
    @nicesql.update("update person set name={name} where id={id}")
    def update(id: int, name: str) -> int:
        pass

    # noinspection PyShadowingBuiltins
    @staticmethod
    @nicesql.delete("delete from person where id={id}")
    def delete(id: int) -> int:
        pass

    def test_insert(self):
        name = "insert001"
        new_id = TestCRUDWithSta.insert(name)

        person = TestCRUDWithSta.get(new_id)
        assert person
        assert person.name == name

    def test_delete(self):
        name = "delete001"
        new_id = TestCRUDWithSta.insert(name)
        person = TestCRUDWithSta.get(new_id)
        assert person
        assert person.name == name
        assert TestCRUDWithSta.delete(new_id) == 1
        person = TestCRUDWithSta.get(new_id)
        assert person is None

    def test_update(self):
        name = "update001"
        update_name = "update002"
        new_id = TestCRUDWithSta.insert(name)
        person = TestCRUDWithSta.get(new_id)
        assert person
        assert person.name == name
        assert TestCRUDWithSta.update(new_id, update_name) == 1
        person = TestCRUDWithSta.get(new_id)
        assert person
        assert person.name == update_name
