-- tsql sql:
DECLARE @sql nvarchar(max);
SELECT @sql = 'DBCC CHECKIDENT (''' + table_name + ''', NORESEED)'
FROM (VALUES ('customer')) AS temp_result (table_name);
EXEC sp_executesql @sql
