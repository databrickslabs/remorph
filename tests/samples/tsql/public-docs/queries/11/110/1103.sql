-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-queue-transact-sql?view=sql-server-ver16

CREATE QUEUE ExpenseQueue
    ON ExpenseWorkFileGroup;