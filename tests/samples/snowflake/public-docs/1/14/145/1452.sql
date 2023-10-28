select *
  from table(information_schema.auto_refresh_registration_history(
    date_range_start=>dateadd('day',-14,current_date()),
    date_range_end=>current_date(),
    object_type=>'external_table'));