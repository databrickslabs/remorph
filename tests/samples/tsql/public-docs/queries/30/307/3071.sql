-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-master-key-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
ALTER MASTER KEY REGENERATE WITH ENCRYPTION BY PASSWORD = 'dsjdkflJ435907NnmM#sX003';
GO