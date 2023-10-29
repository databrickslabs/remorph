-- see https://learn.microsoft.com/en-us/sql/t-sql/lesson-1-creating-database-objects?view=sql-server-ver16

-- The basic syntax for reading data from a single table
SELECT ProductID, ProductName, Price, ProductDescription
    FROM dbo.Products
GO