-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-server-audit-transact-sql?view=sql-server-ver16

SELECT spt.[name], spt.[number]
FROM   [master].[dbo].[spt_values] spt
WHERE  spt.[type] = N'EOD'
ORDER BY spt.[name];