select *
  from table(information_schema.external_functions_history(
    date_range_start => to_timestamp_ltz('2020-05-24 12:00:00.000'),
    date_range_end => to_timestamp_ltz('2020-05-24 12:30:00.000')));