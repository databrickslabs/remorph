USE AdventureWorks2022;  
GO  
SELECT name, SCHEMA_NAME(schema_id) AS SchemaName  
FROM sys.objects  
WHERE type = 'U'  
ORDER BY SchemaName;