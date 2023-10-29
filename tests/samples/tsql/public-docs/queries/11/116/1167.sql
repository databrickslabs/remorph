-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-statistics-transact-sql?view=sql-server-ver16

CREATE STATISTICS ContactPromotion1
    ON Person.Person (BusinessEntityID, LastName, EmailPromotion)
WHERE EmailPromotion = 2
WITH SAMPLE 50 PERCENT;
GO