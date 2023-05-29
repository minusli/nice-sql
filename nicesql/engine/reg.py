from typing import Dict, Type

from nicesql.engine.base import Engine
from nicesql.engine.impl_mysql import MysqlEngine
from nicesql.engine.impl_sqlite import SqliteEngine
from nicesql.utils import parse_db_url
from nicesql.utils.error import NotFoundError, UnsupportedError

__engines: Dict[str, Engine] = {}
__engine_type_map: Dict[str, Type[Engine]] = {
    "mysql": MysqlEngine,
    "sqlite": SqliteEngine,
}


def register_engine(**kwargs: Type[Engine]):
    for schema, engine in kwargs.items():
        __engine_type_map[schema.strip()] = engine


def add_db(**kwargs: str):
    for alias, url in kwargs.items():
        params = parse_db_url(url)
        engine_type = __engine_type_map.get(params["type"], "")
        if not engine_type:
            raise UnsupportedError(f'engine type unsupported: type={engine_type}')

        __engines[alias] = engine_type(**params)


def get_db(alias="default") -> Engine:
    if alias not in __engines:
        raise NotFoundError(f'engine not found: alias={alias}')

    return __engines[alias]
