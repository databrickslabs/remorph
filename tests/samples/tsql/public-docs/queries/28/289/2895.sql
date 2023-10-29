-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

SELECT i.object_id, i.name, t.object_id, t.name, i.type_desc
FROM sys.indexes i
INNER JOIN sys.tables t ON i.object_id = t.object_id
WHERE i.type_desc = 'CLUSTERED'
AND t.name = 'xdimProduct';