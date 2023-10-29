-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/fulltextserviceproperty-transact-sql?view=sql-server-ver16

EXEC sp_fulltext_service @action='verify_signature', @value=1;  
GO