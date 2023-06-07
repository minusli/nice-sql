import threading
from typing import Any

_tls = threading.local()


def get(key: str, default=None):
    return getattr(_tls, key, default)


def put(key: str, value: Any = None):
    setattr(_tls, key, value)


def pop(key: str, default=None):
    result = get(key, default)
    if hasattr(_tls, key):
        delattr(_tls, key)
    return result