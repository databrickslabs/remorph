-- see https://docs.snowflake.com/en/sql-reference/info-schema/event_tables

SELECT TABLE_NAME
    FROM mydatabase.information_schema.event_tables;