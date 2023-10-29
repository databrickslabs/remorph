-- see https://docs.snowflake.com/en/sql-reference/sql/create-view

CREATE OR REPLACE SECURE VIEW myview COMMENT='Test secure view' AS SELECT col1, col2 FROM mytable;

SELECT is_secure FROM information_schema.views WHERE table_name = 'MYVIEW';