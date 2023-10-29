-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/case-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks

UPDATE dbo.DimEmployee
SET VacationHours = (
        CASE
            WHEN ((VacationHours - 10.00) < 0) THEN VacationHours + 40
            ELSE (VacationHours + 20.00)
            END
        )
WHERE SalariedFlag = 0;
GO