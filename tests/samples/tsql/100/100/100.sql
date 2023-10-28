USE AdventureWorks2022;  
GO  
-- Specifying variables for OFFSET and FETCH values    
DECLARE @RowsToSkip TINYINT = 2
      , @FetchRows TINYINT = 8;  
SELECT DepartmentID, Name, GroupName  
FROM HumanResources.Department  
ORDER BY DepartmentID ASC   
    OFFSET @RowsToSkip ROWS   
    FETCH NEXT @FetchRows ROWS ONLY;