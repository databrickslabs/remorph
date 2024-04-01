from sqlglot.dialects.dialect import Dialect, Dialects

from databricks.labs.remorph.snow import databricks, experimental, snowflake


class DialectConfig:
    _SQLGLOT_DIALECTS = {
        "bigquery": Dialects.BIGQUERY,
        "databricks": databricks.Databricks,
        "experimental": experimental.Databricks,
        "drill": Dialects.DRILL,
        "mssql": Dialects.TSQL,
        "netezza": Dialects.POSTGRES,
        "oracle": Dialects.ORACLE,
        "postgresql": Dialects.POSTGRES,
        "presto": Dialects.PRESTO,
        "redshift": Dialects.REDSHIFT,
        "snowflake": snowflake.Snow,
        "sqlite": Dialects.SQLITE,
        "teradata": Dialects.TERADATA,
        "trino": Dialects.TRINO,
        "vertica": Dialects.POSTGRES,
    }

    def _get_dialect(self, engine: str) -> Dialect:
        return Dialect.get_or_raise(self._SQLGLOT_DIALECTS.get(engine))

    def get_read_dialect(self, config):
        return self._get_dialect(config.source)

    def get_write_dialect(self, config):
        if config.mode == "experimental":
            return self._get_dialect("experimental")
        return self._get_dialect("databricks")
