-- see https://docs.snowflake.com/en/sql-reference/functions/object_keys

SELECT OBJECT_KEYS(object1), OBJECT_KEYS(variant1) 
    FROM objects_1
    ORDER BY id;