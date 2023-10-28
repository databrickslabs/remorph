select *
  from table(information_schema.materialized_view_refresh_history(
    date_range_start=>dateadd(H, -12, current_timestamp)));