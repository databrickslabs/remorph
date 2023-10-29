-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/receive-transact-sql?view=sql-server-ver16

RECEIVE conversation_handle, message_type_name, message_body  
FROM ExpenseQueue ;