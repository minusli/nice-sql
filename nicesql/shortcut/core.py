import inspect
from typing import Callable, Any

from nicesql.engine import get_engine
from nicesql.engine.base import Result

ResultProcessor = Callable[[Result], Any]


def execute(nsql: str, engine='default', **kwargs) -> Result:
    return get_engine(alias=engine).execute(nsql, kwargs)


def bind(nsql: str, engine: str = 'default', processor: ResultProcessor = None):
    def _bind(func):
        func_sig = inspect.signature(func)

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
            result = get_engine(alias=engine).execute(nsql, kwargs)
            if processor:
                return processor(result)
            return result

        return wrap

    return _bind
