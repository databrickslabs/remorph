
-- snowflake sql:
SELECT TO_NUMERIC(col1, 15, 5) AS col1 FROM sales_reports;

-- databricks sql:
SELECT CAST(col1 AS DECIMAL(15, 5)) AS col1 FROM sales_reports;
