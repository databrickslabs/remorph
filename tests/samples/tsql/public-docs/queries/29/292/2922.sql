-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/object-name-transact-sql?view=sql-server-ver16

SELECT name, object_id, type_desc  
FROM sys.objects  
WHERE name = OBJECT_NAME(274100017);