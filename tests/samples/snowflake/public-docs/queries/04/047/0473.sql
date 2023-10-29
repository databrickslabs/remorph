-- see https://docs.snowflake.com/en/sql-reference/sql/create-table

CREATE TABLE example (col1 NUMBER COMMENT 'a column comment') COMMENT='a table comment';


SHOW TABLES LIKE 'example';


DESC TABLE example;
