
-- snowflake sql:
SELECT TO_DECIMAL(col1, '$999.099'),
                TO_NUMERIC(tbl.col2, '$999,099.99') FROM dummy tbl;

-- databricks sql:
SELECT TO_NUMBER(col1, '$999.099'),
        TO_NUMBER(tbl.col2, '$999,099.99') FROM dummy AS tbl;
