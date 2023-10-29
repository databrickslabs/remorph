-- see https://docs.snowflake.com/en/sql-reference/functions/external_table_registration_history

select *
  from table(information_schema.external_table_file_registration_history(
    start_time=>dateadd('hour',-1,current_timestamp()),
    table_name=>'mydb.public.external_table_name'));