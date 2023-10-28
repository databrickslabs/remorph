select *
  from table(information_schema.search_optimization_history(
    date_range_start=>dateadd(D, -7, current_date),
    date_range_end=>current_date)
    );