import logging
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Result, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class DatabaseConnector(ABC):
    @abstractmethod
    def _connect(self) -> Engine:
        pass

    @abstractmethod
    def execute_query(self, query: str) -> Result[Any]:
        pass


class _BaseConnector(DatabaseConnector):
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


def _create_connector(db_type: str, config: dict[str, Any]) -> DatabaseConnector:
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
        # pylint: disable=import-outside-toplevel
        import snowflake.sqlalchemy  # type: ignore
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization

        # Snowflake does not follow a traditional SQL Alchemy connection string URL; they have their own.
        # e.g.,   connection_string = (f"snowflake://{user}:{pw}@{account}")
        # https://docs.snowflake.com/en/developer-guide/python-connector/sqlalchemy
        sqlalchemy_driver = "snowflake"
        url_parts = self.config["server"].split(".")
        parsed_url = f"{url_parts[0]}.{url_parts[1]}.{url_parts[2]}"
        connection_string = snowflake.sqlalchemy.URL(
            drivername=sqlalchemy_driver,
            account=parsed_url,
            user=self.config["user"],
            database=self.config["database"],
            schema=self.config["schema"],
            warehouse=self.config["warehouse"],
        )

        # Users can optionally specify a private key to use
        if "private_key_path" in self.config:
            logging.info("Reading private key from filesystem path.")
            with open(self.config["private_key_path"], "rb") as key:
                p_key = serialization.load_pem_private_key(key.read(), password=None, backend=default_backend())
            key_bytes = p_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )

            engine = create_engine(connection_string, connect_args={"private_key": key_bytes})
        else:
            engine = create_engine(connection_string)

        return engine


class MSSQLConnector(_BaseConnector):
    def _connect(self) -> Engine:
        query_params = {"driver": self.config['driver']}

        for key, value in self.config.items():
            if key not in ["user", "password", "server", "database", "port"]:
                query_params[key] = value
        connection_string = URL.create(
            "mssql+pyodbc",
            username=self.config['user'],
            password=self.config['password'],
            host=self.config['server'],
            port=self.config.get('port', 1433),
            database=self.config['database'],
            query=query_params,
        )
        return create_engine(connection_string)


class DatabaseManager:
    def __init__(self, db_type: str, config: dict[str, Any]):
        self.connector = _create_connector(db_type, config)

    def execute_query(self, query: str) -> Result[Any]:
        try:
            return self.connector.execute_query(query)
        except OperationalError:
            logger.error("Error connecting to the database check credentials")
            raise ConnectionError("Error connecting to the database check credentials") from None

    def check_connection(self) -> bool:
        query = "SELECT 101 AS test_column"
        result = self.execute_query(query)
        row = result.fetchone()
        if row is None:
            return False
        return row[0] == 101
