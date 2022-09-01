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

import nicesql
from nicesql import Sqlite, SqlModel
from typing import List

nicesql.register(Sqlite(":memory:"))


class Person(SqlModel):
    def __init__(self):
        self.id = None
        self.name = None


@nicesql.ddl("""
    create table if not exists person(
        id      integer not null primary key,
        name    varchar(127)
    )
""")
def create_person_table():
    pass


@nicesql.insert("insert into person(name) values ({name})")
def insert(name) -> int:
    pass


@nicesql.select("select * from person where id={id}", model=Person, first=True)
def get(id) -> Person:
    pass


@nicesql.select("select * from person where name like {name}", model=Person)
def find(name) -> List[Person]:
    pass


@nicesql.update("update person set name={name} where id={id}")
def update_name(id: int, name: str) -> int:
    pass


@nicesql.delete("delete from person where name={name}")
def delete(name: str) -> int:
    pass


if __name__ == '__main__':
    create_person_table()  # create person table

    id = insert("name001")  # id=1
    person = get(id)  # person=Person(id=1, name=name001)

    rowcount = update_name(id, "name002")  # rowcount=1
    person = get(id)  # person=Person(id=1, name=name002)

    rowcount = delete("name002")  # rowcount=1
    person = get(id)  # person=None

    insert("name003")
    insert("name004")
    persons = find("name%")  # persons=[Person(id=2, name=name003), Person(id=3, name=name004)]

    # #############################
    # also you can use execute api
    # #############################
    persons = nicesql.execute("select * from person where name like {name}", name="name%").all(model=Person)  # persons=[Person(id=2, name=name003), Person(id=3, name=name004)]

    new_id = nicesql.execute("insert into person(name) values({name})", name="name005").insertid()  # new_id = 4

    rowcount = nicesql.execute(
        "update person set name={name} where id = {id}", name="name006", id=new_id
    )  # rowcount = 1
```
