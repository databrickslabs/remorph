-- see https://docs.snowflake.com/en/sql-reference/functions/automatic_clustering_history

select *
  from table(information_schema.automatic_clustering_history(
    date_range_start=>dateadd(H, -12, current_timestamp)));