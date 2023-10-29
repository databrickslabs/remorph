-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16

BEGIN TRANSACTION

SELECT COUNT(*)
FROM HumanResources.Employee WITH (TABLOCK, HOLDLOCK);