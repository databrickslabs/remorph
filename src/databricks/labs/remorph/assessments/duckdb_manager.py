import duckdb


class DuckDBManager:
    """Manages a connection to a single DuckDB database instance."""

    _instance = None
    _connection = None

    def __new__(cls, db_path: str = "remorph_profiler_db.duckdb"):
        if cls._instance is None:
            cls._instance = super(DuckDBManager, cls).__new__(cls)
            cls._instance._init_connection(db_path)
        return cls._instance

    def _init_connection(self, db_path: str):
        self._db_path = db_path
        self._connection = duckdb.connect(database=db_path)

    def get_connection(self):
        return self._connection

    def close_connection(self):
        if self._connection is not None:
            self._connection.close()
            DuckDBManager._instance = None
            DuckDBManager._connection = None
