from typing import Type

from nicesql.shortcut.core import bind


def select(nsql: str, engine: str = 'default', model: Type = None, first: bool = False):
    return bind(nsql=nsql, engine=engine, processor=lambda r: r.first(model=model) if first else r.all(model=model))


def insert(nsql: str, engine: str = 'default'):
    return bind(nsql=nsql, engine=engine, processor=lambda result: result.insertid())


def update(nsql: str, engine: str = 'default'):
    return bind(nsql=nsql, engine=engine, processor=lambda result: result.rowcount())


def delete(nsql: str, engine: str = 'default'):
    return update(nsql=nsql, engine=engine)


def ddl(nsql: str, engine: str = 'default'):
    return bind(nsql=nsql, engine=engine)
