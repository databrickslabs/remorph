-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/case-transact-sql?view=sql-server-ver16

SELECT BusinessEntityID,
    SalariedFlag
FROM HumanResources.Employee
ORDER BY CASE SalariedFlag
        WHEN 1 THEN BusinessEntityID
        END DESC,
    CASE
        WHEN SalariedFlag = 0 THEN BusinessEntityID
        END;
GO