-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/session-user-transact-sql?view=sql-server-ver16

DECLARE @session_usr NCHAR(30);  
SET @session_usr = SESSION_USER;  
SELECT 'This session''s current user is: '+ @session_usr;  
GO