-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/and-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT  BusinessEntityID, LoginID, JobTitle, VacationHours   
FROM HumanResources.Employee  
WHERE JobTitle = 'Marketing Assistant'  
AND VacationHours > 41 ;