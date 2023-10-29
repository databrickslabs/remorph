-- see https://docs.snowflake.com/en/sql-reference/functions/is_object

SELECT IS_OBJECT(object1), IS_OBJECT(array1), IS_OBJECT(boolean1) FROM multiple_types;