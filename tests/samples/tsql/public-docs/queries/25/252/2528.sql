-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datediff-transact-sql?view=sql-server-ver16

SELECT DATEDIFF(millisecond, GETDATE(), SYSDATETIME());