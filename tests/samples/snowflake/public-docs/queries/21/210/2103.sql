-- see https://docs.snowflake.com/en/sql-reference/functions/query_history

select *
  from table(information_schema.query_history(
    END_TIME_RANGE_START=>to_timestamp_ltz('2017-12-4 12:00:00.000 -0700'),
    END_TIME_RANGE_END=>to_timestamp_ltz('2017-12-4 12:30:00.000 -0700')));