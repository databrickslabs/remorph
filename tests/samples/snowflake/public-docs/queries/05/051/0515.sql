-- see https://docs.snowflake.com/en/sql-reference/sql/create-clone

CREATE TABLE orders_clone_restore CLONE orders AT (TIMESTAMP => TO_TIMESTAMP_TZ('04/05/2013 01:02:03', 'mm/dd/yyyy hh24:mi:ss'));