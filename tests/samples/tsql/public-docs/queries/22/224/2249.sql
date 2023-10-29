-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/receive-transact-sql?view=sql-server-ver16

RECEIVE TOP (1) * FROM ExpenseQueue ;