import inspect
from typing import Callable, Dict, Any


def extract_valid_params(fn: Callable, *args, **kwargs) -> Dict[str, Any]:
    fn_sig = inspect.signature(fn)
    fn_bound = fn_sig.bind(*args, **kwargs)
    kwargs: Dict[str, Any] = {}
    for _name, _param in fn_sig.parameters.items():
        _value = _param.default
        if _name in fn_bound.arguments:
            _value = fn_bound.arguments[_name]
        if _value == _param.empty:
            continue
        if _param.kind == inspect.Parameter.VAR_KEYWORD:
            kwargs.update(_value)
        else:
            kwargs[_name] = _value

    return kwargs
