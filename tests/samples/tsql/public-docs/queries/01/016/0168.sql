-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/like-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks

SELECT BusinessEntityID,
    FirstName,
    LastName
FROM Person.Person
WHERE FirstName LIKE '[CS]heryl';
GO