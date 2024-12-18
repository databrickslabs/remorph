-- tsql sql:
DECLARE @sql nvarchar(max) = '';
SELECT @sql += 'DROP TABLE ' + QUOTENAME(name) + ';'
FROM (
    VALUES ('#t1'), ('#t2'), ('#t3'), ('#t4'), ('#t5'), ('#t6')
) AS t (name);
EXEC sp_executesql @sql;
