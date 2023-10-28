SELECT state, bushels_produced, ROW_NUMBER()
  OVER (ORDER BY bushels_produced DESC)
  FROM corn_production;
