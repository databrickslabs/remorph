-- see https://docs.snowflake.com/en/sql-reference/functions/automatic_clustering_history

select *
  from table(information_schema.automatic_clustering_history(
    date_range_start=>dateadd(D, -7, current_date),
    date_range_end=>current_date,
    table_name=>'mydb.myschema.mytable'));