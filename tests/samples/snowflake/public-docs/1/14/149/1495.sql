select database_name, credits_used, bytes_transferred
  from table(information_schema.database_replication_usage_history(
    date_range_start=>'2023-03-28 12:00:00.000 +0000',
    date_range_end=>'2023-03-28 12:30:00.000 +0000'));