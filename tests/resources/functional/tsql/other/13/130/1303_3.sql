-- tsql sql:
DECLARE @sql nvarchar(max);
SELECT @sql = 'DROP TABLE ' + tableName
FROM (
    VALUES ('table_name')
) AS temp(tableName);
EXEC sp_executesql @sql;
