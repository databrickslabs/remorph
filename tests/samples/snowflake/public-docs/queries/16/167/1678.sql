-- see https://docs.snowflake.com/en/sql-reference/info-schema/class_instances

SELECT name, class_name, class_schema_name, class_database_name
    FROM mydatabase.INFORMATION_SCHEMA.CLASS_INSTANCES;