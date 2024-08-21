
-- snowflake sql:
SELECT zeroifnull(col1) AS pcol1 FROM tabl;

-- databricks sql:
SELECT IF(col1 IS NULL, 0, col1) AS pcol1 FROM tabl;
