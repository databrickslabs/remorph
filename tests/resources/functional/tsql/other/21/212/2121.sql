--Query type: DCL
DECLARE @sql NVARCHAR(MAX);
SELECT @sql = 'GRANT EXECUTE ON ' + name + ' TO John;'
FROM (
    VALUES ('pr_Names')
) AS procedures(name);
EXEC sp_executesql @sql;
