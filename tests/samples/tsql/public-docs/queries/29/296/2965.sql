-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/begin-dialog-conversation-transact-sql?view=sql-server-ver16

SELECT service_broker_guid  
FROM sys.databases  
WHERE database_id = DB_ID() ;