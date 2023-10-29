-- see https://docs.snowflake.com/en/sql-reference/functions/is_decimal

SELECT IS_DECIMAL(decimal1), IS_DECIMAL(integer1), IS_DECIMAL(double1) FROM multiple_types;