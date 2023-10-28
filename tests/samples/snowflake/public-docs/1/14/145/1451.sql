select *
  from table(information_schema.auto_refresh_registration_history(
    date_range_start=>to_timestamp_tz('2021-06-17 12:00:00.000 -0700'),
    date_range_end=>to_timestamp_tz('2021-06-17 12:30:00.000 -0700'),
    object_type=>'external_table'));