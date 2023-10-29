-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/equals-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT DepartmentID, Name  
FROM HumanResources.Department  
WHERE GroupName = 'Manufacturing';