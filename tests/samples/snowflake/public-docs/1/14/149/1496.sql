select database_name, credits_used, bytes_transferred
  from table(information_schema.database_replication_usage_history(
    date_range_start=>dateadd(H, -12, current_timestamp)));