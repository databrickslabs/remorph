-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/connections-transact-sql?view=sql-server-ver16

SELECT GETDATE() AS 'Today''s Date and Time',   
@@CONNECTIONS AS 'Login Attempts';