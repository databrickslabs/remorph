-- tsql sql:
DECLARE @username sysname = 'RMeyyappan';
DECLARE @sql nvarchar(max) = N'REVOKE VIEW DEFINITION ON LOGIN::EricKurjan FROM ''' + @username + ''' CASCADE;'
EXEC sp_executesql @sql;
