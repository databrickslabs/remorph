select *
  from table(information_schema.external_table_file_registration_history(
    start_time=>dateadd('hour',-1,current_timestamp()),
    table_name=>'mydb.public.external_table_name'));