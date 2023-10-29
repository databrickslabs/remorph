-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/return-transact-sql?view=sql-server-ver16

DECLARE @return_status INT;  
EXEC @return_status = checkstate '6';  
SELECT 'Return Status' = @return_status;  
GO