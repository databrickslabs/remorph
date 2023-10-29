-- see https://docs.snowflake.com/en/sql-reference/functions/object_construct

SELECT OBJECT_CONSTRUCT(*) AS oc
    FROM demo_table_1
    ORDER BY oc['PROVINCE'];