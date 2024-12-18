-- tsql sql:
DECLARE @sql nvarchar(max) = N'SELECT * FROM (VALUES (1, ''test1'', ''test2'')) AS temp_table (id, name, description)'; EXEC sys.sp_executesql @sql;
