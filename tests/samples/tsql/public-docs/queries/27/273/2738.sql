-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16

SELECT RTRIM(p.FirstName) + ' ' + LTRIM(p.LastName) AS Name,
    d.City
FROM Person.Person AS p
INNER JOIN HumanResources.Employee e
    ON p.BusinessEntityID = e.BusinessEntityID
INNER JOIN (
    SELECT bea.BusinessEntityID,
        a.City
    FROM Person.Address AS a
    INNER JOIN Person.BusinessEntityAddress AS bea
        ON a.AddressID = bea.AddressID
    ) AS d
    ON p.BusinessEntityID = d.BusinessEntityID
ORDER BY p.LastName,
    p.FirstName;