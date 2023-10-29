-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/like-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks
  
SELECT LastName,
    FirstName
FROM Person.Person
WHERE LastName LIKE 'Zh[ae]ng'
ORDER BY LastName ASC,
    FirstName ASC;
GO