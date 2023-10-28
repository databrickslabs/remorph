SELECT n, scale, FLOOR(n, scale)
  FROM test_floor
  ORDER BY n, scale;