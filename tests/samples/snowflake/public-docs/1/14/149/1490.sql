select *
  from table(information_schema.replication_usage_history(
    date_range_start=>'2019-02-10 12:00:00.000 +0000',
    date_range_end=>'2019-02-10 12:30:00.000 +0000'));