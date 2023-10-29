-- see https://docs.snowflake.com/en/sql-reference/functions/data_transfer_history

select *
  from table(information_schema.data_transfer_history(
    date_range_start=>dateadd('hour',-12,current_timestamp())));