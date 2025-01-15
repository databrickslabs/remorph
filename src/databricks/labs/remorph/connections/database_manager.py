from abc import ABC, abstractmethod
from pathlib import Path
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class ISourceSystemConnector(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute_query(self, query: str):
        pass

class SnowflakeConnector(ISourceSystemConnector):
    def __init__(self, config):
        self.config = config
        self.engine = None

    def connect(self):
        connection_string = (
            f"snowflake://{self.config['user']}:{self.config['password']}@{self.config['account']}/"
            f"{self.config['database']}/{self.config['schema']}?warehouse={self.config['warehouse']}&role={self.config['role']}"
        )
        self.engine = create_engine(connection_string)

    def execute_query(self, query: str):
        if not self.engine:
            raise ConnectionError("Not connected to the database.")
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            result = session.execute(query)
            return [dict(row) for row in result]
        finally:
            session.close()

class MSSQLConnector(ISourceSystemConnector):
    def __init__(self, config):
        self.config = config
        self.engine = None

    def connect(self):
        connection_string = (
            f"mssql+pyodbc://{self.config['user']}:{self.config['password']}@{self.config['server']}/"
            f"{self.config['database']}?driver={self.config['driver']}"
        )
        self.engine = create_engine(connection_string)

    def execute_query(self, query: str):
        if not self.engine:
            raise ConnectionError("Not connected to the database.")
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            result = session.execute(query)
            return [dict(row) for row in result]
        finally:
            session.close()


#TODO move this factory to Application Context
class SourceSystemConnectorFactory:
    @staticmethod
    def create_connector(db_type: str, config: dict) -> ISourceSystemConnector:
        if db_type == "snowflake":
            return SnowflakeConnector(config)
        elif db_type == "mssql":
            return MSSQLConnector(config)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

