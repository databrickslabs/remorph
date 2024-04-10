
-- snowflake sql:
SELECT t.n, nullifzero(t.n) AS pcol1 FROM tbl t;

-- databricks sql:
SELECT t.n, IF(t.n = 0, NULL, t.n) AS pcol1 FROM tbl AS t;
