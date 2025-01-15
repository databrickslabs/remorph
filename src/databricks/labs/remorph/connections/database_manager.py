from abc import ABC, abstractmethod
from pathlib import Path
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Any

class _ISourceSystemConnector(ABC):
    @abstractmethod
    def connect(self) -> Engine:
        pass

    @abstractmethod
    def execute_query(self, query: str) -> list[dict[str, Any]]:
        pass

class _BaseConnector(_ISourceSystemConnector):
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.engine = None

    def connect(self) -> Engine:
        raise NotImplementedError("Subclasses should implement this method")

    def execute_query(self, query: str) -> list[dict[str, Any]]:
        if not self.engine:
            raise ConnectionError("Not connected to the database.")
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            result = session.execute(query)
            return [dict(row) for row in result]
        finally:
            session.close()

class SnowflakeConnector(_BaseConnector):
    def connect(self) -> Engine:
        connection_string = (
            f"snowflake://{self.config['user']}:{self.config['password']}@{self.config['account']}/"
            f"{self.config['database']}/{self.config['schema']}?warehouse={self.config['warehouse']}&role={self.config['role']}"
        )
        self.engine = create_engine(connection_string)

class MSSQLConnector(_BaseConnector):
    def connect(self) -> Engine:
        connection_string = (
            f"mssql+pyodbc://{self.config['user']}:{self.config['password']}@{self.config['server']}/"
            f"{self.config['database']}?driver={self.config['driver']}"
        )
        self.engine = create_engine(connection_string)

#TODO: Move this application context
class SourceSystemConnectorFactory:
    @staticmethod
    def create_connector(db_type: str, config: dict[str, str]) -> ISourceSystemConnector:
        if db_type == "snowflake":
            return SnowflakeConnector(config)
        elif db_type == "mssql":
            return MSSQLConnector(config)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
