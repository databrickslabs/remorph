-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16

ALTER INDEX PK_Department_DepartmentID ON HumanResources.Department REBUILD;