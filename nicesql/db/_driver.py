from abc import ABC, abstractmethod
from typing import List, Dict, Any


class LiteDriver(ABC):
    def __init__(self, hostname: str, port: int, username: str, password: str, database: str, **kwargs):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.kwargs = kwargs

    @abstractmethod
    def connection(self) -> "LiteConnection":
        pass


class LiteConnection(ABC):
    @abstractmethod
    def begin(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def cursor(self) -> "LiteCursor":
        pass

    @abstractmethod
    def close(self):
        pass


class LiteCursor(ABC):
    @abstractmethod
    def execute(self, sql: str, params: List[Any]):
        pass

    @abstractmethod
    def lastrowid(self) -> int | str:
        pass

    @abstractmethod
    def rowcount(self) -> int:
        pass

    @abstractmethod
    def fetchall(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def close(self):
        pass
