SELECT
  wswscs.d_week_seq AS d_week_seq1,
  sun_sales AS sun_sales1,
  mon_sales AS mon_sales1
FROM wswscs, date_dim
WHERE
  date_dim.d_week_seq = wswscs.d_week_seq AND d_year = 2001
;
