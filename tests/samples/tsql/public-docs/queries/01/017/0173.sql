-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/like-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks

SELECT p.FirstName,
    p.LastName,
    ph.PhoneNumber
FROM Person.PersonPhone AS ph
INNER JOIN Person.Person AS p
    ON ph.BusinessEntityID = p.BusinessEntityID
WHERE ph.PhoneNumber NOT LIKE '415%'
    AND p.FirstName = 'Gail'
ORDER BY p.LastName;
GO