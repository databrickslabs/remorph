-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-trigger-transact-sql?view=sql-server-ver16

IF (ROWCOUNT_BIG() = 0)
RETURN;