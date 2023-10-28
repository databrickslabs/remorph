SELECT
    p, o, i,
    COUNT(i) OVER (PARTITION BY p ORDER BY o) count_i_Range_Pre,
    SUM(i)   OVER (PARTITION BY p ORDER BY o) sum_i_Range_Pre,
    AVG(i)   OVER (PARTITION BY p ORDER BY o) avg_i_Range_Pre,
    MIN(i)   OVER (PARTITION BY p ORDER BY o) min_i_Range_Pre,
    MAX(i)   OVER (PARTITION BY p ORDER BY o) max_i_Range_Pre
  FROM example_cumulative
  ORDER BY p,o;