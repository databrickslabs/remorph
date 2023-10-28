CREATE OR REPLACE SECURE VIEW myview COMMENT='Test secure view' AS SELECT col1, col2 FROM mytable;

SELECT is_secure FROM information_schema.views WHERE table_name = 'MYVIEW';