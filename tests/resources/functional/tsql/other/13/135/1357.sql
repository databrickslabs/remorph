-- tsql sql:
DECLARE @users TABLE (email nvarchar(255));
INSERT INTO @users (email)
VALUES ('alice@example.com');
DECLARE @email nvarchar(255);
SELECT @email = email
FROM @users;
DECLARE @sql nvarchar(max);
SET @sql = 'CREATE LOGIN [' + @email + '] WITH PASSWORD = ''password''';
EXEC sp_executesql @sql;
SET @sql = 'CREATE USER [' + @email + '] FOR LOGIN [' + @email + ']';
EXEC sp_executesql @sql;
SELECT *
FROM @users;
-- REMORPH CLEANUP: DROP LOGIN [alice@example.com];
-- REMORPH CLEANUP: DROP USER [alice@example.com];
