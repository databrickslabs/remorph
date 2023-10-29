-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/dateadd-transact-sql?view=sql-server-ver16

SELECT DATEADD(month,-(10/2), SYSDATETIME());