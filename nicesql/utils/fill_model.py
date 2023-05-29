import inspect
from typing import TypeVar

T = TypeVar("T")


def fill_model(model: T, **kwargs) -> T:
    for k, v in kwargs.items():
        if not hasattr(model, k):
            continue

        origin_v = getattr(model, k, None)
        if origin_v and inspect.ismethod(origin_v):
            continue

        setattr(model, k, v)

    return model
