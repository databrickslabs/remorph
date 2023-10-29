-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-search-property-list-transact-sql?view=sql-server-ver16

CREATE SEARCH PROPERTY LIST JobCandidateProperties 
FROM AdventureWorks2022.DocumentPropertyList;  
GO  
ALTER FULLTEXT INDEX ON HumanResources.JobCandidate   
   SET SEARCH PROPERTY LIST JobCandidateProperties;  
GO