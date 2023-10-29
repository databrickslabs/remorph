-- see https://docs.snowflake.com/en/sql-reference/functions/is_array

SELECT IS_ARRAY(array1), IS_ARRAY(array2), IS_ARRAY(boolean1) 
    FROM multiple_types;