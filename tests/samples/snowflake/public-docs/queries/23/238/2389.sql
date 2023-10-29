-- see https://docs.snowflake.com/en/sql-reference/data-types-datetime

select ts + INTERVAL '4 seconds' from t1 where ts > to_timestamp('2014-04-05 01:02:03');