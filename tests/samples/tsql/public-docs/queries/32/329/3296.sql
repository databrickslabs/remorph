-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-fulltext-index-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
DROP FULLTEXT INDEX ON HumanResources.JobCandidate;  
GO