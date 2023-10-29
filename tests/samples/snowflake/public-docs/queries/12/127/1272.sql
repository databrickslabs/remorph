-- see https://docs.snowflake.com/en/sql-reference/functions/object_construct_keep_null

SELECT OBJECT_CONSTRUCT(*) AS oc,
       OBJECT_CONSTRUCT_KEEP_NULL(*) AS oc_keep_null
    FROM demo_table_1
    ORDER BY oc_keep_null['PROVINCE'];