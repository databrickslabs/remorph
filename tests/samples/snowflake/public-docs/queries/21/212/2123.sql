-- see https://docs.snowflake.com/en/sql-reference/functions/data_transfer_history

select *
  from table(mydb.information_schema.data_transfer_history(
    date_range_start=>to_timestamp_tz('2017-10-24 12:00:00.000 -0700'),
    date_range_end=>to_timestamp_tz('2017-10-24 12:30:00.000 -0700')));