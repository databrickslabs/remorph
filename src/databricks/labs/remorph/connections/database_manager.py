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
    # TODO: Not Implemented
    def _connect(self) -> Engine:
        raise NotImplementedError("Snowflake connector not implemented")


class MSSQLConnector(_BaseConnector):
    def _connect(self) -> Engine:
        connection_string = (
            f"mssql+pyodbc://{self.config['user']}:{self.config['password']}@{self.config['server']}/"
            f"{self.config['database']}?driver={self.config['driver']}"
        )
        # TODO: Add support for other connection parameters through a custom dictionary or config
        self.engine = create_engine(connection_string, echo=True, connect_args=None)
        return self.engine


# TODO Refactor into application context
class DatabaseManager:
    def __init__(self, db_type: str, config: dict[str, str]):
        self.db_type = db_type
        self.config = config
        self.connector = self._create_connector()

    def _create_connector(self) -> _ISourceSystemConnector:
        if self.db_type.lower() == "snowflake":
            return SnowflakeConnector(self.config)
        if self.db_type.lower() in {"mssql", "tsql", "synapse"}:
            return MSSQLConnector(self.config)
        raise ValueError(f"Unsupported database type: {self.db_type}")

    def execute_query(self, query: str) -> Result[Any]:
        return self.connector.execute_query(query)
