-- see https://docs.snowflake.com/en/sql-reference/functions/time_from_parts

select time_from_parts(0, 100, 0), time_from_parts(12, 0, 12345);
