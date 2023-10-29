-- see https://docs.snowflake.com/en/sql-reference/snowflake-db-classes

ALTER USER SET SEARCH_PATH = '$current, $public, SNOWFLAKE.ML';