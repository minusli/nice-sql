from typing import Dict
from typing import Type
from urllib.parse import urlparse, parse_qs

from nicesql.engine import Engine
from nicesql.engine._engines import MysqlEngine, SqliteEngine
from nicesql.utils.error import NotFoundError, UnsupportedError, DuplicateError

__databases: Dict[str, Engine] = {}
__engines: Dict[str, Type[Engine]] = {
    "mysql": MysqlEngine,
    "sqlite": SqliteEngine,
}


def register_engine(schema: str, engine: Type[Engine]):
    __engines[schema] = engine


def add_db(url: str, alias: str = "default"):
    if alias in __databases:
        raise DuplicateError(f"duplicate db: alias={alias}")
    params = parse_db_url(url)
    engine = __engines.get(params["type"])
    if not engine:
        raise UnsupportedError(f'engine unsupported: type={params["type"]}')

    # noinspection PyArgumentList
    __databases[alias] = engine(**params)


def get_db(alias="default") -> Engine:
    if alias not in __databases:
        raise NotFoundError(f'db not found: alias={alias}')

    return __databases[alias]


def remove_db(alias: str = "default"):
    if alias in __databases:
        __databases.pop(alias)


def parse_db_url(url: str) -> Dict[str, str | int]:
    url = url.strip()
    r = urlparse(url)
    engine_type = r.scheme
    engine_host = r.hostname
    engine_port = r.port
    engine_database = r.path.strip("/")
    engine_params = parse_qs(r.query)

    kv = {}
    for k, v in engine_params.items():
        if v:
            kv[k] = v[0]

    kv['type'] = engine_type
    kv['host'] = engine_host
    kv['port'] = engine_port
    kv['database'] = engine_database

    return kv
