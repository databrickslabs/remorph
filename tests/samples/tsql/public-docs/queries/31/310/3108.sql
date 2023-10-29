-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/case-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

UPDATE HumanResources.Employee
SET VacationHours = (
        CASE
            WHEN ((VacationHours - 10.00) < 0) THEN VacationHours + 40
            ELSE (VacationHours + 20.00)
            END
        )
OUTPUT Deleted.BusinessEntityID,
    Deleted.VacationHours AS BeforeValue,
    Inserted.VacationHours AS AfterValue
WHERE SalariedFlag = 0;
GO