-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datefirst-transact-sql?view=sql-server-ver16

SET LANGUAGE Italian;  
GO  
SELECT @@DATEFIRST;  
GO  
SET LANGUAGE us_english;  
GO  
SELECT @@DATEFIRST;