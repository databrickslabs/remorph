-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/output-clause-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

DECLARE @MyTableVar TABLE (
    ProductID INT NOT NULL,
    ProductName NVARCHAR(50) NOT NULL,
    ProductModelID INT NOT NULL,
    PhotoID INT NOT NULL
);

DELETE Production.ProductProductPhoto
OUTPUT DELETED.ProductID,
    p.Name,
    p.ProductModelID,
    DELETED.ProductPhotoID
INTO @MyTableVar
OUTPUT DELETED.ProductID,
    DELETED.ProductPhotoID,
    GETDATE() AS DeletedDate
FROM Production.ProductProductPhoto AS ph
INNER JOIN Production.Product AS p
    ON ph.ProductID = p.ProductID
WHERE p.ProductID BETWEEN 800
        AND 810;

--Display the results of the table variable.
SELECT ProductID,
    ProductName,
    PhotoID,
    ProductModelID
FROM @MyTableVar;
GO