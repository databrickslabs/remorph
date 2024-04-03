
-- source:
SELECT DIV0(a, b);

-- databricks_sql:
SELECT IF(b = 0, 0, a / b);
