-- see https://docs.snowflake.com/en/sql-reference/functions/to_array

INSERT INTO array_demo_2 (ID, array1, array2) 
    SELECT 1, TO_ARRAY(1), TO_ARRAY(3);