-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/greater-than-or-equal-to-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT DepartmentID, Name  
FROM HumanResources.Department  
WHERE DepartmentID >= 13  
ORDER BY DepartmentID;