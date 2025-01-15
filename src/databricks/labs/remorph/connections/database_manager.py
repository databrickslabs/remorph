from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Result
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


class _ISourceSystemConnector(ABC):
    @abstractmethod
    def _connect(self) -> Engine:
        pass

    @abstractmethod
    def execute_query(self, query: str) -> Result[Any]:
        pass


class _BaseConnector(_ISourceSystemConnector):
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.engine: Engine = self._connect()

    def _connect(self) -> Engine:
        raise NotImplementedError("Subclasses should implement this method")

    def execute_query(self, query: str) -> Result[Any]:
        if not self.engine:
            raise ConnectionError("Not connected to the database.")
        session = sessionmaker(bind=self.engine)
        connection = session()
        return connection.execute(text(query))


class SnowflakeConnector(_BaseConnector):
    def _connect(self) -> Engine:
        connection_string = (
            f"snowflake://{self.config['user']}:{self.config['password']}@{self.config['account']}/"
            f"{self.config['database']}/{self.config['schema']}?warehouse={self.config['warehouse']}&role={self.config['role']}"
        )
        self.engine = create_engine(connection_string)
        return self.engine


class MSSQLConnector(_BaseConnector):
    def _connect(self) -> Engine:
        connection_string = (
            f"mssql+pyodbc://{self.config['user']}:{self.config['password']}@{self.config['server']}/"
            f"{self.config['database']}?driver={self.config['driver']}"
        )
        self.engine = create_engine(connection_string)
        return self.engine


class SourceSystemConnectorFactory:
    @staticmethod
    def create_connector(db_type: str, config: dict[str, str]) -> _ISourceSystemConnector:
        if db_type == "snowflake":
            return SnowflakeConnector(config)
        if db_type == "mssql":
            return MSSQLConnector(config)

        raise ValueError(f"Unsupported database type: {db_type}")
