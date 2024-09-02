--Query type: DML
DECLARE @newColumnName NVARCHAR(255) = 'client''s "custom" name';
DECLARE @newSql NVARCHAR(MAX) = 'SELECT value AS ' + QUOTENAME(@newColumnName) + ' FROM (VALUES (''Mike''), (''Emma'')) AS clients(value)';
EXEC sp_executesql @newSql;

SELECT * FROM (VALUES ('Mike'), ('Emma')) AS clients(value);
-- REMORPH CLEANUP: No tables are created in this query