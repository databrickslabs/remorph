-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-fulltext-catalog-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
CREATE FULLTEXT CATALOG ftCatalog AS DEFAULT;  
GO  
CREATE FULLTEXT INDEX ON HumanResources.JobCandidate(Resume) KEY INDEX PK_JobCandidate_JobCandidateID;  
GO