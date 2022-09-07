import inspect
from typing import Callable, Any, Type

from nicesql import utils
from nicesql.sqlengine import get_engine
from nicesql.sqlmodel import SqlModel
from nicesql.sqlresult import SqlResult


def execute(nsql: str, engine='default', **kwargs) -> SqlResult:
    sql, params = utils.parsesql(nsql)
    real_params = [utils.getvalue(kwargs, p) for p in params]
    return get_engine(alias=engine).execute(sql, real_params)


def bind(nsql: str, engine: str = 'default', result_process: Callable[[SqlResult], Any] = None):
    def _bind(func):
        sql, params = utils.parsesql(nsql)
        func_sig = inspect.signature(func)
        # check
        for name, param in func_sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                raise Exception(f"func({func}) not support *args: {name}")

        def wrap(*args, **kwargs):
            func_bound = func_sig.bind(*args, **kwargs)

            kwargs = {}
            for _name, _param in func_sig.parameters.items():
                _value = _param.default
                if _name in func_bound.arguments:
                    _value = func_bound.arguments[_name]
                if _value == _param.empty:
                    continue
                if _param.kind == inspect.Parameter.VAR_KEYWORD:
                    kwargs.update(_value)
                else:
                    kwargs[_name] = _value
            real_params = [utils.getvalue(kwargs, p) for p in params]

            result = get_engine(alias=engine).execute(sql, real_params)
            if result_process:
                return result_process(result)
            return result

        return wrap

    return _bind


def select(nsql: str, engine: str = 'default', model: Type[SqlModel] = None, first: bool = False):
    return bind(
        nsql=nsql, engine=engine,
        result_process=lambda result: result.first(model=model) if first else result.all(model=model)
    )


def insert(nsql: str, engine: str = 'default'):
    return bind(nsql=nsql, engine=engine, result_process=lambda result: result.insertid())


def update(nsql: str, engine: str = 'default'):
    return bind(nsql=nsql, engine=engine, result_process=lambda result: result.rowcount())


def delete(nsql: str, engine: str = 'default'):
    return update(nsql=nsql, engine=engine)
