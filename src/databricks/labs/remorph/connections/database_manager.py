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


def _create_connector(db_type: str, config: dict[str, Any]) -> _ISourceSystemConnector:
    connectors = {
        "snowflake": SnowflakeConnector,
        "mssql": MSSQLConnector,
        "tsql": MSSQLConnector,
        "synapse": MSSQLConnector,
    }

    connector_class = connectors.get(db_type.lower())

    if connector_class is None:
        raise ValueError(f"Unsupported database type: {db_type}")

    return connector_class(config)


class SnowflakeConnector(_BaseConnector):
    def _connect(self) -> Engine:
        raise NotImplementedError("Snowflake connector not implemented")


class MSSQLConnector(_BaseConnector):
    def _connect(self) -> Engine:
        connection_string = (
            f"mssql+pyodbc://{self.config['user']}:{self.config['password']}@{self.config['server']}/"
            f"{self.config['database']}?driver={self.config['driver']}"
        )
        return create_engine(connection_string, echo=True)


class DatabaseManager:
    def __init__(self, db_type: str, config: dict[str, Any]):
        self.connector = _create_connector(db_type, config)

    def execute_query(self, query: str) -> Result[Any]:
        return self.connector.execute_query(query)
