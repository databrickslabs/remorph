-- tsql sql:
DECLARE @sql nvarchar(max) = '';
SELECT @sql += 'DROP MESSAGE TYPE ' + QUOTENAME(MessageType) + ';
' FROM (VALUES ('MessageType1'), ('MessageType2')) AS MessageTypes(MessageType);
EXEC sp_executesql @sql;
