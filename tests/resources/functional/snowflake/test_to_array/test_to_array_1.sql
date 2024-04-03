
-- source:
SELECT to_array(col1) AS ary_col;

-- databricks_sql:
SELECT IF(col1 IS NULL, NULL, ARRAY(col1)) AS ary_col;
