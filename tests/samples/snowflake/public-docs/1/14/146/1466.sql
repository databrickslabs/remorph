select *
  from table(information_schema.automatic_clustering_history(
    date_range_start=>'2018-04-10 13:00:00.000 -0700',
    date_range_end=>'2018-04-10 14:00:00.000 -0700'));