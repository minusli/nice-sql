import inspect
import types
from abc import ABCMeta, abstractmethod
from typing import List

from nicesql import utils
from nicesql.sqlresult import SqlResult


class SQLEngine(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, sql: str, params: List) -> SqlResult:
        pass

    @abstractmethod
    def close(self):
        pass


engines = {}


def register(engine: SQLEngine, alias="default"):
    if alias in engines:
        raise Exception(f"Duplicate Engine: alias={alias}")
    engines[alias] = engine


def get_engine(alias='default') -> SQLEngine:
    if alias not in engines:
        raise Exception(f"Not Found Engine: alias={alias}")
    return engines[alias]


def close(alias='default'):
    engine = get_engine(alias=alias)
    engine.close()
    del engines[alias]


def execute(nsql: str, engine='default', **kwargs) -> SqlResult:
    sql, params = utils.parsesql(nsql)
    params = [utils.getvalue(kwargs, p) for p in params]
    return get_engine(alias=engine).execute(sql, params)


def _check_with_decorator(func):
    if not isinstance(func, types.FunctionType):
        raise Exception(f"func({func}) must be function")
    arguments = inspect.getargs(func.__code__)
    if arguments.varargs:
        raise Exception(f"func({func}) not support *args: {arguments.varargs}")
    if arguments.varkw:
        raise Exception(f"func({func}) not support *args: {arguments.varkw}")


def _merge_args_kwargs_with_decorator(func, *args, **kwargs):
    func_params = inspect.getargs(func.__code__).args
    if len(func_params) != len(args):
        raise Exception(f"func({func}) define against use")
    if func_params and func_params[0] in ('self', 'cls'):
        func_params = func_params[1:]
        args = args[1:]
    for i, k in enumerate(func_params):
        if k not in kwargs:
            kwargs[k] = args[i]
    return kwargs


def select(nsql: str, engine='default', model=None, first=False):
    def _select(func):
        sql, params = utils.parsesql(nsql)
        _check_with_decorator(func)

        def wrap(*args, **kwargs):
            kwargs = _merge_args_kwargs_with_decorator(func, *args, **kwargs)
            real_params = [utils.getvalue(kwargs, p) for p in params]

            result = get_engine(alias=engine).execute(sql, real_params)
            if first:
                return result.first(model=model)
            return result.all(model=model)

        return wrap

    return _select


def update(nsql: str, engine='default'):
    def _update(func):
        sql, params = utils.parsesql(nsql)
        _check_with_decorator(func)

        def wrap(*args, **kwargs):
            kwargs = _merge_args_kwargs_with_decorator(func, *args, **kwargs)
            real_params = [utils.getvalue(kwargs, p) for p in params]

            result = get_engine(alias=engine).execute(sql, real_params)
            return result.rowcount()

        return wrap

    return _update


def delete(nsql: str, engine='default'):
    return update(nsql=nsql, engine=engine)


def insert(nsql: str, engine='default'):
    def _insert(func):
        sql, params = utils.parsesql(nsql)
        _check_with_decorator(func)

        def wrap(*args, **kwargs):
            kwargs = _merge_args_kwargs_with_decorator(func, *args, **kwargs)
            real_params = [utils.getvalue(kwargs, p) for p in params]

            result = get_engine(alias=engine).execute(sql, real_params)
            return result.insertid()

        return wrap

    return _insert


def ddl(nsql: str, engine='default'):
    def _sql(func):
        sql, params = utils.parsesql(nsql)
        _check_with_decorator(func)

        def wrap(*args, **kwargs):
            kwargs = _merge_args_kwargs_with_decorator(func, *args, **kwargs)
            real_params = [utils.getvalue(kwargs, p) for p in params]

            get_engine(alias=engine).execute(sql, real_params)

        return wrap

    return _sql
