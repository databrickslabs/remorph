
-- snowflake sql:
SELECT TRY_TO_DECIMAL(col1, '$999.099'),
                TRY_TO_NUMERIC(tbl.col2, '$999,099.99') FROM dummy tbl;

-- databricks sql:
SELECT CAST(TRY_TO_NUMBER(col1, '$999.099') AS DECIMAL(38, 0)),
        CAST(TRY_TO_NUMBER(tbl.col2, '$999,099.99') AS DECIMAL(38, 0)) FROM dummy AS tbl;
