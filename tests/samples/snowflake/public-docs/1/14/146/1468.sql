select *
  from table(information_schema.automatic_clustering_history(
    date_range_start=>dateadd(D, -7, current_date),
    date_range_end=>current_date));