import inspect
from typing import Callable, Dict, Any, Optional, Type, List

from nicesql.engine import execute, Result, Model, Row


def select(nsql: str, data: Any = None) -> "Select":
    return Select(nsql, data)


def update(nsql: str, data: Any = None) -> "Update":
    return Update(nsql, data)


def delete(nsql: str, data: Any = None) -> "Update":
    return Update(nsql, data)


def insert(nsql: str, data: Any = None) -> "Insert":
    return Insert(nsql, data)


def ddl(nsql: str, data: Any = None) -> "DDL":
    return DDL(nsql, data)


def sql(nsql: str, data: Any = None) -> "SQL":
    return SQL(nsql, data)


class SQL:
    def __init__(self, nsql: str, data: Any = None):
        self.__nsql: str = nsql
        self.__data: Any = data
        self.__db: str = "default"

    def execute(self, data: Any = None) -> Result:
        data = data or self.__data
        return execute(self.__nsql, data=data, db=self.__db)

    def __call__(self, fn: Callable) -> Callable:
        def wrap(*args, **kwargs):
            data = extract_valid_params(fn, *args, **kwargs)
            return self.execute(data=data)

        return wrap

    def db(self, db="default") -> "SQL":
        self.__db = db
        return self


class Select(SQL):
    def __init__(self, nsql: str, data: Any = None):
        super().__init__(nsql, data)

        self.__model: Optional[Type[Model]] = None
        self.__first: bool = False

    def execute(self, data: Any = None) -> List[Row | Model] | Row | Model:
        result = super().execute(data)
        if self.__first:
            return result.first(self.__model)
        return result.all(self.__model)

    def model(self, model: Type[Model]) -> "Select":
        self.__model = model
        return self

    def first(self, model: Type[Model] = None) -> "Select":
        self.__first = True
        if model:
            self.__model = model
        return self


class Update(SQL):
    def __init__(self, nsql: str, data: Any = None):
        super().__init__(nsql, data)

    def execute(self, data: Any = None) -> int:
        result = super().execute(data)
        return result.rowcount()


class Insert(SQL):
    def __init__(self, nsql: str, data: Any = None):
        super().__init__(nsql, data)

    def execute(self, data: Any = None) -> Any:
        result = super().execute(data)
        return result.insertid()


class DDL(SQL):
    def __init__(self, nsql: str, data: Any = None):
        super().__init__(nsql, data)

    def execute(self, data: Any = None) -> None:
        super().execute(data)


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
