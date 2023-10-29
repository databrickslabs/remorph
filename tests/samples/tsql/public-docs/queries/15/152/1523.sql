-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/receive-transact-sql?view=sql-server-ver16

DECLARE @conversation_group_id UNIQUEIDENTIFIER ;  
  
SET @conversation_group_id =   
    <retrieve conversation group ID from database> ;  
  
RECEIVE *  
FROM ExpenseQueue  
WHERE conversation_group_id = @conversation_group_id ;