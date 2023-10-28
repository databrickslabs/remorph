SELECT k, MIN(d), MAX(d)
  FROM minmax_example 
  GROUP BY k
  ORDER BY k;