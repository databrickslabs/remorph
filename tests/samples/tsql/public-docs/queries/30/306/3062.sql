-- see https://learn.microsoft.com/en-us/sql/t-sql/lesson-1-creating-database-objects?view=sql-server-ver16

UPDATE dbo.Products
    SET ProductName = 'Flat Head Screwdriver'
    WHERE ProductID = 50
GO