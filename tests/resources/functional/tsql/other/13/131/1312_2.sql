--Query type: DML
CREATE TABLE test_table (id int);
DECLARE @sql nvarchar(max) = N'CREATE TRIGGER trig_test ON test_table FOR INSERT AS BEGIN END;';
EXEC sp_executesql @sql;
DECLARE @trigger_name nvarchar(50) = (SELECT name FROM (VALUES ('trig_test')) AS trig(name));
DECLARE @enable_sql nvarchar(max) = N'ALTER TABLE test_table ENABLE TRIGGER ' + @trigger_name;
EXEC sp_executesql @enable_sql;
SELECT * FROM test_table;
-- REMORPH CLEANUP: DROP TABLE test_table;
-- REMORPH CLEANUP: DROP TRIGGER trig_test;
