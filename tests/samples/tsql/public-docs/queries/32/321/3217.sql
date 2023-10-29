-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/update-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  

--Display the initial data of the table to be updated.  
SELECT BusinessEntityID, VacationHours, ModifiedDate, HireDate  
FROM HumanResources.Employee
WHERE VacationHours < 10  
GO  

DECLARE @MyTableVar TABLE (  
    EmpID int NOT NULL,  
    OldVacationHours smallint,  
    NewVacationHours smallint,  
    ModifiedDate datetime);  
UPDATE HumanResources.Employee  
SET VacationHours =  VacationHours * 1.25,  
    ModifiedDate = GETDATE()   
OUTPUT inserted.BusinessEntityID,  
      deleted.VacationHours,  
      inserted.VacationHours,  
      inserted.ModifiedDate  
INTO @MyTableVar
    WHERE VacationHours < 10  
--Display the result set of the table variable.  
SELECT EmpID, OldVacationHours
, NewVacationHours, ModifiedDate  
FROM @MyTableVar;  

GO  
--Display the result set of the table.  
SELECT BusinessEntityID, VacationHours, ModifiedDate, HireDate  
FROM HumanResources.Employee
    WHERE VacationHours < 10  
GO