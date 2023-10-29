-- see https://docs.snowflake.com/en/sql-reference/info-schema/external_tables

SELECT table_name, last_altered FROM mydatabase.information_schema.external_tables;