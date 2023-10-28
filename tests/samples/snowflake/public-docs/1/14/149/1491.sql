select *
  from table(information_schema.replication_usage_history(
    date_range_start=>dateadd(H, -12, current_timestamp)));