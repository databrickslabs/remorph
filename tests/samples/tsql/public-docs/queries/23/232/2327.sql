-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/declare-local-variable-transact-sql?view=sql-server-ver16

SELECT *
FROM tempdb.sys.indexes
WHERE object_id < 0;
GO