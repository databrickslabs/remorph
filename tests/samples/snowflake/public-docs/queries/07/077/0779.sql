-- see https://docs.snowflake.com/en/sql-reference/functions/as_char-varchar

SELECT 
       AS_ARRAY(array1) AS "ARRAY1",
       AS_ARRAY(array2) AS "ARRAY2",
       AS_BOOLEAN(boolean1) AS "BOOLEAN",
       AS_CHAR(char1) AS "CHAR",
       AS_DECIMAL(decimal1, 6, 3) AS "DECIMAL",
       AS_DOUBLE(double1) AS "DOUBLE",
       AS_INTEGER(integer1) AS "INTEGER",
       AS_OBJECT(object1) AS "OBJECT",
       AS_ARRAY(object1) AS "OBJECT AS ARRAY"
  FROM multiple_types;