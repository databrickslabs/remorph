-- see https://docs.snowflake.com/en/sql-reference/functions/is_double-real

SELECT IS_DOUBLE(double1), IS_DOUBLE(decimal1), IS_DOUBLE(integer1), IS_DOUBLE(boolean1) FROM multiple_types;