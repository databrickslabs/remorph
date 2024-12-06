-- tsql sql:
WITH tables AS ( SELECT 'table1' AS name UNION ALL SELECT 'table2' AS name ) SELECT * FROM ( VALUES ('table1'), ('table2') ) AS t (name) WHERE t.name IN ( SELECT name FROM tables );
