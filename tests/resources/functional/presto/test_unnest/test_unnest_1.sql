-- presto sql:
SELECT
  *
FROM
  default.sync_gold
  CROSS JOIN UNNEST(engine_waits) t (col1, col2)
WHERE
  ("cardinality"(engine_waits) > 0);

-- databricks sql:
SELECT
  *
FROM
  default.sync_gold LATERAL VIEW EXPLODE(engine_waits) As col1,
  col2
WHERE
  (SIZE(engine_waits) > 0);
