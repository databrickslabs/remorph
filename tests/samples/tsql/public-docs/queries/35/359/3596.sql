-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/count-transact-sql?view=sql-server-ver16

USE ssawPDW;
  
SELECT DepartmentName,
    COUNT(EmployeeKey)AS EmployeesInDept
FROM dbo.DimEmployee
GROUP BY DepartmentName
HAVING COUNT(EmployeeKey) > 15;