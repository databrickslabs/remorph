-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/get-conversation-group-transact-sql?view=sql-server-ver16

DECLARE @conversation_group_id UNIQUEIDENTIFIER ;  
  
GET CONVERSATION GROUP @conversation_group_id  
FROM AdventureWorks.dbo.ExpenseQueue ;