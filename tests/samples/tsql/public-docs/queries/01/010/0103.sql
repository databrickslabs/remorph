-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-table-transact-sql?view=sql-server-ver16

-- Optional: Create MASTER KEY if it doesn't exist in the database:
CREATE MASTER KEY ENCRYPTION BY PASSWORD = '<Strong Password>'
GO