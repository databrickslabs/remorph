-- see https://docs.snowflake.com/en/sql-reference/functions/is_integer

SELECT IS_INTEGER(integer1), IS_INTEGER(decimal1), IS_INTEGER(double1) FROM multiple_types;