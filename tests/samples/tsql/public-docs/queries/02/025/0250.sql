-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/less-than-or-equal-to-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT DepartmentID, Name  
FROM HumanResources.Department  
WHERE DepartmentID <= 3  
ORDER BY DepartmentID;