-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/receive-transact-sql?view=sql-server-ver16

DECLARE @conversation_handle UNIQUEIDENTIFIER ;  
  
SET @conversation_handle = <retrieve conversation from database> ;  
  
RECEIVE *  
FROM ExpenseQueue  
WHERE conversation_handle = @conversation_handle ;