-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/comment-transact-sql?view=sql-server-ver16

-- Choose the AdventureWorks2022 database.  
USE AdventureWorks2022;  
GO  
-- Choose all columns and all rows from the Address table.  
SELECT *  
FROM Person.Address  
ORDER BY PostalCode ASC; -- We do not have to specify ASC because   
-- that is the default.  
GO