from sqlglot import Dialects, Dialect

from databricks.labs.remorph.reconcile.dialects import oracle, presto, snowflake
from databricks.labs.remorph.reconcile.dialects.databricks import Databricks

SQLGLOT_DIALECTS: dict[str, type[Dialect] | str] = {
    "athena": Dialects.ATHENA,
    "bigquery": Dialects.BIGQUERY,
    "databricks": Databricks,
    "mysql": Dialects.MYSQL,
    "netezza": Dialects.POSTGRES,
    "oracle": oracle.Oracle,
    "postgresql": Dialects.POSTGRES,
    "presto": presto.Presto,
    "redshift": Dialects.REDSHIFT,
    "snowflake": snowflake.Snowflake,
    "sqlite": Dialects.SQLITE,
    "teradata": Dialects.TERADATA,
    "trino": Dialects.TRINO,
    "tsql": Dialects.TSQL,
    "vertica": Dialects.POSTGRES,
}


def get_dialect(dialect: str) -> Dialect:
    return Dialect.get_or_raise(SQLGLOT_DIALECTS.get(dialect))


def get_dialect_name(dialect: Dialect) -> str:
    try:
        return Dialects(dialect).value
    except ValueError:
        return "universal"


def dialect_exists(name: str) -> bool:
    return SQLGLOT_DIALECTS.get(name, None) is not None
