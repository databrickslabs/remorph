select *
  from table(information_schema.auto_refresh_registration_history(
    date_range_start=>dateadd('hour',-12,current_timestamp()),
    object_type=>'external_table',
    object_name=>'myexttable'));