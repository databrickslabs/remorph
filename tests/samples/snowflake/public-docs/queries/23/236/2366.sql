-- see https://docs.snowflake.com/en/sql-reference/functions/timestamp_from_parts

select timestamp_ntz_from_parts(2013, 4, 5, 12, 00, 00, 987654321);