-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/output-clause-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

DECLARE @MyTableVar TABLE (
    EmpID INT NOT NULL,
    OldVacationHours INT,
    NewVacationHours INT,
    VacationHoursDifference INT,
    ModifiedDate DATETIME);
  
UPDATE TOP (10) HumanResources.Employee
SET VacationHours = VacationHours * 1.25,
    ModifiedDate = GETDATE()
OUTPUT INSERTED.BusinessEntityID,
       DELETED.VacationHours,
       INSERTED.VacationHours,
       INSERTED.VacationHours - DELETED.VacationHours,
       INSERTED.ModifiedDate
INTO @MyTableVar;
  
--Display the result set of the table variable.
SELECT EmpID, OldVacationHours, NewVacationHours,
    VacationHoursDifference, ModifiedDate
FROM @MyTableVar;
GO
SELECT TOP (10) BusinessEntityID, VacationHours, ModifiedDate
FROM HumanResources.Employee;
GO