
-- snowflake sql:
SELECT TRY_TO_NUMERIC(sm.col1, '$999.00', 15, 5) AS col1,
                TRY_TO_NUMBER(sm.col2, '$99.00', 15, 5) AS col2 FROM sales_reports sm;

-- databricks sql:
SELECT CAST(TRY_TO_NUMBER(sm.col1, '$999.00') AS DECIMAL(15, 5)) AS col1,
        CAST(TRY_TO_NUMBER(sm.col2, '$99.00') AS DECIMAL(15, 5)) AS col2 FROM sales_reports AS sm;
