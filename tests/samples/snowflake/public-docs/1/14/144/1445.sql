select *
  from table(information_schema.external_table_file_registration_history(
    start_time=>cast('2022-04-25' as timestamp),
    table_name=>'mydb.public.external_table_name'));