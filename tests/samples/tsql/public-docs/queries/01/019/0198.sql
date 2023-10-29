-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/begin-end-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  

DECLARE @Iteration Integer = 0;
WHILE @Iteration <10  
BEGIN  
    SELECT FirstName, MiddleName   
    FROM dbo.DimCustomer WHERE LastName = 'Adams';
    SET @Iteration += 1  ;
END;