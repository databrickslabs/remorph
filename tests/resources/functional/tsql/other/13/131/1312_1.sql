-- tsql sql:
DECLARE @sql nvarchar(max) = '';

WITH trig_example AS (
    SELECT 'trig_example' AS table_name, 'trig1' AS trigger_name
)

SELECT @sql = 'ALTER TABLE ' + QUOTENAME(table_name) + ' DISABLE TRIGGER ' + QUOTENAME(trigger_name) + ';' FROM trig_example;

EXEC sp_executesql @sql;

SELECT * FROM sys.tables;

SELECT * FROM sys.triggers;

-- REMORPH CLEANUP: DROP TABLE IF EXISTS trig_example;
