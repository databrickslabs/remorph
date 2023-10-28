INSERT ALL
  INTO t1 VALUES ($1, an_alias, "10 + 20")
SELECT 1, 50 AS an_alias, 10 + 20;