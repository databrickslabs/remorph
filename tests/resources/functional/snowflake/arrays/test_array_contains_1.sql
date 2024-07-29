
-- snowflake sql:
SELECT array_contains(33, arr_col) AS array_contains_col1 FROM tabl;

-- databricks sql:
SELECT ARRAY_CONTAINS(arr_col, 33) AS array_contains_col1 FROM tabl;
