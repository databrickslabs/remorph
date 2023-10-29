-- see https://learn.microsoft.com/en-us/sql/t-sql/lesson-1-creating-database-objects?view=sql-server-ver16

-- Dropping the optional dbo and dropping the ProductDescription column
INSERT Products (ProductID, ProductName, Price)
    VALUES (3000, '3 mm Bracket', 0.52)
GO