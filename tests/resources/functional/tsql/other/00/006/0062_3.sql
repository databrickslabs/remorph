-- tsql sql:
DECLARE @sql nvarchar(max);
SELECT @sql = N'CREATE DATABASE ' + QUOTENAME(database_name) + '; USE DATABASE ' + QUOTENAME(database_name) + '; USE SCHEMA ' + QUOTENAME(schema_name) + ';'
FROM (
    VALUES ('ex2_gor_y', 'PUBLIC')
) AS temp_result(database_name, schema_name);
EXEC sp_executesql @sql;
