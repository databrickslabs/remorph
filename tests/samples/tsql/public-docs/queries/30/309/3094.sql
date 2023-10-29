-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/case-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

SELECT JobTitle,
    MAX(ph1.Rate) AS MaximumRate
FROM HumanResources.Employee AS e
INNER JOIN HumanResources.EmployeePayHistory AS ph1
    ON e.BusinessEntityID = ph1.BusinessEntityID
GROUP BY JobTitle
HAVING (
        MAX(CASE
                WHEN SalariedFlag = 1 THEN ph1.Rate
                ELSE NULL
                END) > 40.00
        OR MAX(CASE
                WHEN SalariedFlag = 0 THEN ph1.Rate
                ELSE NULL
                END) > 15.00
        )
ORDER BY MaximumRate DESC;
GO