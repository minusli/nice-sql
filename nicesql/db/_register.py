from typing import Dict, Type, Any

import dsnparse

from nicesql.db._driver import LiteDriver
from nicesql.db._driver_mysql import Mysql
from nicesql.db._driver_sqlite import Sqlite

__dbs: Dict[str, LiteDriver] = {}
__dbtypes: Dict[str, Type[LiteDriver]] = {
    "mysql": Mysql,
    "sqlite": Sqlite
}


def register_driver(schema: str, engine: Type[LiteDriver]):
    __dbtypes[schema] = engine


def add_db(dsn: str, alias="default"):
    dsn = _parse_dsn(dsn)
    # noinspection PyArgumentList
    __dbs[alias] = __dbtypes[dsn.driver](hostname=dsn.hostname, port=dsn.port, username=dsn.username, password=dsn.password,
                                         database=dsn.database, **dsn.params)


def get_db(alias="default") -> LiteDriver:
    return __dbs[alias]


class _DSN:
    def __init__(self, driver: str, username: str, password: str, hostname: str, port: int, database: str, params=Dict[str, Any]):
        self.driver = driver
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port
        self.database = database
        self.params = params


def _parse_dsn(dsn: str) -> _DSN:
    dsn = dsnparse.parse(dsn)
    return _DSN(
        driver=dsn.scheme,
        username=dsn.username,
        password=dsn.password,
        hostname=dsn.hostname,
        port=dsn.port,
        database=dsn.database.strip("/") if dsn.database else dsn.database,
        params=dsn.query_params
    )


if __name__ == '__main__':
    _parse_dsn("a+prom.interface.postgres.Interface://testuser:testpw@localhost:1234/testdb/xx/?a=1&b=01&c=abc&d=true&e=false&f=1.1&f=1.2")
