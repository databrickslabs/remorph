from sqlglot.dialects.dialect import Dialect, Dialects

from databricks.labs.remorph.snow.databricks import Databricks
from databricks.labs.remorph.snow.snowflake import Snow
from databricks.labs.remorph.snow.databricks_preview import DatabricksPreivew

SQLGLOT_DIALECTS = {
    "bigquery": Dialects.BIGQUERY,
    "databricks": Databricks,
    "databricks_preview": DatabricksPreivew,
    "drill": Dialects.DRILL,
    "mssql": Dialects.TSQL,
    "netezza": Dialects.POSTGRES,
    "oracle": Dialects.ORACLE,
    "postgresql": Dialects.POSTGRES,
    "presto": Dialects.PRESTO,
    "redshift": Dialects.REDSHIFT,
    "snowflake": Snow,
    "sqlite": Dialects.SQLITE,
    "teradata": Dialects.TERADATA,
    "trino": Dialects.TRINO,
    "vertica": Dialects.POSTGRES,
}


def get_dialect(engine: str) -> Dialect:
    return Dialect.get_or_raise(SQLGLOT_DIALECTS.get(engine))
