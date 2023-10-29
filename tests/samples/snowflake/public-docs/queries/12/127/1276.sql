-- see https://docs.snowflake.com/en/sql-reference/functions/object_insert

SELECT OBJECT_INSERT(OBJECT_INSERT(OBJECT_CONSTRUCT(),'k1', 100),'k1','string-value', TRUE) AS obj;
