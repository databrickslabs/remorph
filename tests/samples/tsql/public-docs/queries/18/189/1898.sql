-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/user-transact-sql?view=sql-server-ver16

DECLARE @usr CHAR(30)  
SET @usr = user  
SELECT 'The current user''s database username is: '+ @usr  
GO