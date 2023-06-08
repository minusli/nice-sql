# 使用手册

------

# 如何安装？

`pip install nice-sql`

# 如何使用？

### Step 1: 添加 db 配置

```python
from nicesql.db import add_db

if __name__ == '__main__':
    add_db("mysql://test:test@localhost:3306/test_db?charset=utf8mb4")
```

### step2: 执行 sql

```python
from nicesql.shortcut import select, update, insert, delete, sql


# 方式 1：直接查询
def way1():
    result = select("select * from t where a={a} and b in ({b})", a=1, b=["1", "2"]).execute()


# 方式 2：装饰器查询
@select("select * from t where a={a}")
def get(a=1):
    pass


def way2():
    return get(2)

```

### 扩展功能

- 支持控制返回数据模型:

```python
from nicesql.shortcut import select


class User:
    def __init__(self):
        self.id = None
        self.name = None


if __name__ == '__main__':
    # 使用 model(T) 方法设置数据模型
    users = select("select * from user where id in ({ids})", id=[1, 2, 3]).model(User).execute()
```

- 支持 sql 中扩展列表:

```sql
/*
ids 对应的传参，可以是列表，会被展开成  v1,v2,v3...
但只会展开第一层，不支持递归展开
*/
select *
from t
where id in ({ids})
```

- 支持返回第 1 条数据:

```python
from nicesql.shortcut import select


class User:
    def __init__(self):
        self.id = None
        self.name = None


if __name__ == '__main__':
    # 使用 first(T=None) 控制只获取第一条数据, 同时也可以设置 model
    user = select("select * from user where id={id}", id=1).first(User).execute()
```

- 支持设置多 DB

```python
from nicesql.db import add_db

if __name__ == '__main__':
    # 通过设置别名参数，创建多个 db；
    add_db("mysql://username:password@localhost:3306/test1", "db1")
    add_db("mysql://username:passwprd@localhost:3306/test2", "db2")

    # 使用是通过 db(alias) 指定需要使用的 db 
    from nicesql.shortcut import insert

    insert("insert into t(name) values({name})", name="hello").db("db1").execute()
```

- 占位符支持递归查询，同时支持管道进行数据处理

```python
from nicesql.shortcut import select


class User:
    def __init__(self):
        self.id = 5


if __name__ == '__main__':
    select("select * from t where id={user.id|str}", user=User())
```
