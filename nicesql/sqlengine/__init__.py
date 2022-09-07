from nicesql.sqlengine.base import SqlEngine

engines = {}


def register(engine: SqlEngine, alias="default"):
    if alias in engines:
        raise Exception(f"Duplicate Engine: alias={alias}")
    engines[alias] = engine


def get_engine(alias='default') -> SqlEngine:
    if alias not in engines:
        raise Exception(f"Not Found Engine: alias={alias}")
    return engines[alias]


def close(alias='default'):
    engine = get_engine(alias=alias)
    engine.close()
    del engines[alias]
