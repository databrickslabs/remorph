-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/like-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks
  
SELECT Name
FROM sys.system_views
WHERE Name LIKE 'dm%';
GO