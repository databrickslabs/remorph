select *
  from table(information_schema.automatic_clustering_history(
    date_range_start=>dateadd(H, -12, current_timestamp)));