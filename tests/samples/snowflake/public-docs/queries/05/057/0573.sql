-- see https://docs.snowflake.com/en/sql-reference/sql/create-view

CREATE VIEW myview COMMENT='Test view' AS SELECT col1, col2 FROM mytable;

SHOW VIEWS;
