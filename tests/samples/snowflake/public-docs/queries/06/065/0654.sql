-- see https://docs.snowflake.com/en/sql-reference/functions/array_cat

INSERT INTO array_demo (ID, array1, array2) 
    SELECT 1, ARRAY_CONSTRUCT(1, 2), ARRAY_CONSTRUCT(3, 4);