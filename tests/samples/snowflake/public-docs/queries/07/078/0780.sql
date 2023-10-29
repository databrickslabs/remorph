-- see https://docs.snowflake.com/en/sql-reference/functions/as_array

SELECT 
       AS_ARRAY(array1) AS "ARRAY1",
       AS_ARRAY(array2) AS "ARRAY2",
       AS_OBJECT(object1) AS "OBJECT",
       AS_ARRAY(object1) AS "OBJECT AS ARRAY"
  FROM multiple_types;