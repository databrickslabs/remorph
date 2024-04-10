
-- snowflake sql:
SELECT TO_NUMERIC(sm.col1, '$999.00', 15, 5) AS col1,
                TO_NUMBER(sm.col2, '$99.00', 15, 5) AS col2 FROM sales_reports sm;

-- databricks sql:
SELECT CAST(TO_NUMBER(sm.col1, '$999.00') AS DECIMAL(15, 5)) AS col1,
        CAST(TO_NUMBER(sm.col2, '$99.00') AS DECIMAL(15, 5)) AS col2 FROM sales_reports AS sm;
