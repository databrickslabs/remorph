--Query type: DML
WITH trigger_name AS (SELECT 'tr_Customer' AS name), table_name AS (SELECT 'Customer' AS name) SELECT 'DISABLE TRIGGER ' + (SELECT name FROM trigger_name) + ' ON ' + (SELECT name FROM table_name);
