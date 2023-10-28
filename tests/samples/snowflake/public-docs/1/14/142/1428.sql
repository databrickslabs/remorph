select *
  from table(information_schema.search_optimization_history(
    date_range_start=>dateadd(H, -12, current_timestamp)));