-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/execute-transact-sql?view=sql-server-ver16

USE master; EXEC ('USE AdventureWorks2022; SELECT BusinessEntityID, JobTitle FROM HumanResources.Employee;');