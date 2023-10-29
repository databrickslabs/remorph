-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/context-info-transact-sql?view=sql-server-ver16

SET CONTEXT_INFO 0x1256698456;  
GO  
SELECT CONTEXT_INFO();  
GO