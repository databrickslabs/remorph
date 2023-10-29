-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/percent-character-wildcard-character-s-to-match-transact-sql?view=sql-server-ver16

SELECT FirstName, LastName
FROM Person.Person
WHERE FirstName LIKE 'Dan%';
GO