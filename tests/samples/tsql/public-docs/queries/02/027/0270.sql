-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/add-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT FirstName, LastName, VacationHours, SickLeaveHours,   
    VacationHours + SickLeaveHours AS TotalHoursAway  
FROM DimEmployee  
ORDER BY TotalHoursAway ASC;