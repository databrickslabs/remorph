-- see https://docs.snowflake.com/en/sql-reference/sql/create-clone

CREATE SCHEMA mytestschema_clone_restore CLONE testschema BEFORE (TIMESTAMP => TO_TIMESTAMP(40*365*86400));