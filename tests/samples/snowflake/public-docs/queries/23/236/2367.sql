-- see https://docs.snowflake.com/en/sql-reference/functions/timestamp_from_parts

select timestamp_ntz_from_parts(to_date('2013-04-05'), to_time('12:00:00'));