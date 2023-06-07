import queue
import threading

from nicesql.db import add_db, execute, transaction


def setup_module():
    add_db("mysql://test:test@localhost/test")
    execute("""
            create table if not exists user(
                id      int not null primary key auto_increment,
                name    varchar(127)
            )
            """)


def teardown_module():
    execute("drop table if exists user")


class User:
    def __init__(self, id_=0, name=""):
        self.id = id_
        self.name = name


def test_crud():
    # insert
    user1 = User(name="user1")
    user2 = User(name="user2")
    user1.id = execute("insert into user(name) values({user.name})", user=user1).insertid()
    user2.id = execute("insert into user(name) values({user.name})", user=user2).insertid()

    # read
    user_1 = execute("select * from user where id={id}", id=user1.id).first(User)
    user_2 = execute("select * from user where id={id}", id=user2.id).first(User)
    users = execute("select * from user where id in ({ids})", ids=(user1.id, user2.id)).all(User)
    assert user_1.name == user1.name
    assert user_2.name == user2.name
    for u in users:
        assert u.name in (user1.name, user2.name)

    # delete
    rowcount = execute("delete from user where id={id}", id=user1.id).rowcount()
    assert rowcount == 1
    user_1 = execute("select * from user where id={id}", id=user1.id).first(User)
    assert user_1 is None

    # update
    user2.name = "user2_"
    rowcount = execute("update user set name={user.name} where id={user.id}", user=user2).rowcount()
    assert rowcount == 1
    user_2 = execute("select * from user where id={id}", id=user2.id).first(User)
    assert user_2.name == user2.name


def test_tx():
    results = []
    chan1 = queue.Queue()
    chan2 = queue.Queue()
    name = "tx_user_1"
    name_new = "tx_user_2"

    @transaction()
    def t1():  # 插入数据
        user = User(name=name)
        user.id = execute("insert into user(name) values({user.name})", user=user).insertid()
        user_ = execute("select * from user where id={id}", id=user.id).first(User)
        results.append(user_ is not None and user_.name == user.name)
        chan1.put(1)
        chan2.get()

    def t2():  # 无法看到 t1 的数据
        chan1.get()
        user = execute("select * from user where name={name}", name=name).first(User)
        results.append(user is None)
        chan2.put(1)

    t_1 = threading.Thread(target=t1)
    t_2 = threading.Thread(target=t2)

    t_1.start()
    t_2.start()
    t_1.join()
    t_2.join()

    def t3():  # 能看到 t1 的数据
        user = execute("select * from user where name={name}", name=name).first(User)
        results.append(user is not None)

    t_3 = threading.Thread(target=t3)
    t_3.start()
    t_3.join()

    @transaction()
    def t4():
        rowcount = execute("update user set name={name_new} where name={name}", name=name, name_new=name_new).rowcount()
        results.append(rowcount == 1)
        user = execute("select * from user where name={name_new}", name_new=name_new).first(User)
        results.append(user is not None)
        raise Exception

    t_4 = threading.Thread(target=t4)
    t_4.start()
    t_4.join()

    def t5():
        user = execute("select * from user where name={name}", name=name).first(User)
        results.append(user is not None)
        user = execute("select * from user where name={name_new}", name_new=name_new).first(User)
        results.append(user is None)

    t_5 = threading.Thread(target=t5)
    t_5.start()
    t_5.join()

    assert len(results) == 7
    for r in results:
        assert r
