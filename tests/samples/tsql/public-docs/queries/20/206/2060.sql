-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-synonym-transact-sql?view=sql-server-ver16

EXEC sp_addlinkedserver Server_Remote;
GO
USE tempdb;
GO
CREATE SYNONYM MyEmployee FOR Server_Remote.AdventureWorks2022.HumanResources.Employee;
GO