-- see https://docs.snowflake.com/en/sql-reference/functions/array_compact

INSERT INTO array_demo (ID, array1, array2) 
    SELECT 2, ARRAY_CONSTRUCT(10, NULL, 30), ARRAY_CONSTRUCT(40);