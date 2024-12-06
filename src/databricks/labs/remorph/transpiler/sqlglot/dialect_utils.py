from sqlglot import Dialects, Dialect

from databricks.labs.remorph.transpiler.sqlglot.dialects.oracle import oracle
from databricks.labs.remorph.transpiler.sqlglot.dialects.presto import presto
from databricks.labs.remorph.transpiler.sqlglot.dialects.snowflake import snowflake

SQLGLOT_DIALECTS: dict[str, Dialect] = {
    "athena": Dialects.ATHENA,
    "bigquery": Dialects.BIGQUERY,
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


def get_key_from_dialect(input_dialect: Dialect) -> str:
    return [source_key for source_key, dialect in SQLGLOT_DIALECTS.items() if dialect == input_dialect][0]
