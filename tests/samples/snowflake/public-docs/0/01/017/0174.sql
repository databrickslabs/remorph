SELECT p, o, r AS r_col,
    SUM(r) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 4 PRECEDING AND 2 PRECEDING) sum_r_4P_2P,
    sum(r) over (partition by p ORDER BY o ROWS BETWEEN 2 FOLLOWING AND 4 FOLLOWING) sum_r_2F_4F,
    sum(r) over (partition by p ORDER BY o ROWS BETWEEN 2 PRECEDING AND 4 FOLLOWING) sum_r_2P_4F
  FROM example_sliding
  ORDER BY p, o;