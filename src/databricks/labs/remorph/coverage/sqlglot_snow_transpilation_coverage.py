from sqlglot.dialects.snowflake import Snowflake
from databricks.labs.remorph.coverage import sqlglot_coverage

if __name__ == "__main__":
    sqlglot_coverage.run_coverage(Snowflake, "snowflake")
