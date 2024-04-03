
-- source:
SELECT TO_NUMERIC(col1, 15, 5) AS col1 FROM sales_reports;

-- databricks_sql:
SELECT CAST(col1 AS DECIMAL(15, 5)) AS col1 FROM sales_reports;
