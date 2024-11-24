
-- snowflake sql:
SELECT TRY_TO_DATE('2012.20.12', 'yyyy.dd.MM'), TRY_TO_DATE(d.col1) FROM dummy d;

-- databricks sql:
SELECT DATE(TRY_TO_TIMESTAMP('2012.20.12', 'yyyy.dd.MM')),
        DATE(TRY_TO_TIMESTAMP(d.col1)) FROM dummy AS d;
