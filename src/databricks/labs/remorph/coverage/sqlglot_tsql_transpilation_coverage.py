from sqlglot.dialects.tsql import TSQL
from databricks.labs.remorph.coverage.commons import sqlglot_run_coverage

if __name__ == "__main__":
    sqlglot_run_coverage(TSQL, "tsql")
