-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-procedure-transact-sql?view=sql-server-ver16

CREATE PROC What_DB_is_this
AS
SELECT DB_NAME() AS ThisDB;