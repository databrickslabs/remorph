-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/sql-server-utilities-statements-go?view=sql-server-ver16

-- Yields an error because ; is not permitted after GO  
SELECT @@VERSION;  
GO;