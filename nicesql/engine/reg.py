from typing import Dict, Type

from nicesql.engine.base import Engine
from nicesql.engine.impl_dummy import DummyEngine
from nicesql.engine.impl_mysql import MysqlEngine
from nicesql.engine.impl_sqlite import SqliteEngine
from nicesql.utils import parse_db_url
from nicesql.utils.error import NotFoundError, UnsupportedError, DuplicateError

__engines: Dict[str, Engine] = {}
__engine_type_map: Dict[str, Type[Engine]] = {
    "dummy": DummyEngine,
    "mysql": MysqlEngine,
    "sqlite": SqliteEngine,
}


def reg_engine(url: str, alias="default"):
    if alias in __engines:
        raise DuplicateError(f'engine register duplicate: alias={alias}')

    params = parse_db_url(url)
    engine_type = __engine_type_map.get(params["type"], "")
    if not engine_type:
        raise UnsupportedError(f'engine type unsupported: type={engine_type}')

    __engines[alias] = engine_type()
    __engines[alias].init(**params)


def get_engine(alias="default") -> Engine:
    if alias not in __engines:
        raise NotFoundError(f'engine not found: alias={alias}')

    return __engines[alias]
