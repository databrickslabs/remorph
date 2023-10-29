-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/object-schema-name-transact-sql?view=sql-server-ver16

SELECT QUOTENAME(DB_NAME(db_id()))   
    + N'.'   
    + QUOTENAME(OBJECT_SCHEMA_NAME(object_id, db_id()))   
    + N'.'   
    + QUOTENAME(OBJECT_NAME(object_id, db_id()))  
    , *   
FROM sys.objects;
GO