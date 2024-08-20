
-- snowflake sql:
SELECT OBJECT_CONSTRUCT(*) AS oc FROM demo_table_1 ;

-- databricks sql:
SELECT STRUCT(*) AS oc FROM demo_table_1;
