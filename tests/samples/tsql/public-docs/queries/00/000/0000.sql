-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/begin-conversation-timer-transact-sql?view=sql-server-ver16

-- @dialog_handle is of type uniqueidentifier and  
-- contains a valid conversation handle.  
  
BEGIN CONVERSATION TIMER (@dialog_handle)  
TIMEOUT = 120 ;