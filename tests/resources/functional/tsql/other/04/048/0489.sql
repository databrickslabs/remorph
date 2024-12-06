-- tsql sql:
DECLARE @dbName sysname;
SELECT @dbName = name
FROM (
    VALUES ('newDB')
) AS tempDB(name);
ALTER AUTHORIZATION ON DATABASE::newDB TO [john@newcompany.onmicrosoft.com];
