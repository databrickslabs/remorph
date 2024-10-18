--Query type: DML
DECLARE @MyTableVar TABLE (ProductID INT NOT NULL, ProductName NVARCHAR(50) NOT NULL, ProductModelID INT NOT NULL, PhotoID INT NOT NULL, DeletedDate DATETIME NOT NULL);

WITH ProductCTE AS (
    SELECT 1 AS ProductID, 'Product1' AS Name, 1 AS ProductModelID
    UNION ALL
    SELECT 2, 'Product2', 2
    UNION ALL
    SELECT 3, 'Product3', 3
),
ProductPhotoCTE AS (
    SELECT 1 AS ProductID, 1 AS ProductPhotoID
    UNION ALL
    SELECT 2, 2
    UNION ALL
    SELECT 3, 3
)
INSERT INTO @MyTableVar (ProductID, ProductName, ProductModelID, PhotoID, DeletedDate)
SELECT c.ProductID, c.Name, c.ProductModelID, p.ProductPhotoID, GETDATE() AS DeletedDate
FROM ProductCTE c
INNER JOIN ProductPhotoCTE p ON c.ProductID = p.ProductID
WHERE c.ProductID BETWEEN 1 AND 3;

SELECT * FROM @MyTableVar;
-- REMORPH CLEANUP: DROP TABLE @MyTableVar;