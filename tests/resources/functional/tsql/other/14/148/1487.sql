--Query type: DML
DECLARE @MyTableVar TABLE (ProductID INT NOT NULL, ProductName NVARCHAR(50) NOT NULL, ProductModelID INT NOT NULL, PhotoID INT NOT NULL);

WITH ProductCTE AS (
  SELECT 1 AS ProductID, 'Product1' AS ProductName, 120 AS ProductModelID, 1 AS PhotoID
  UNION ALL
  SELECT 2, 'Product2', 121, 2
  UNION ALL
  SELECT 3, 'Product3', 122, 3
),
ProductProductPhotoCTE AS (
  SELECT 1 AS ProductID, 1 AS ProductPhotoID
  UNION ALL
  SELECT 2, 2
  UNION ALL
  SELECT 3, 3
)
INSERT INTO @MyTableVar (ProductID, ProductName, ProductModelID, PhotoID)
SELECT p.ProductID, p.ProductName, p.ProductModelID, ppp.ProductPhotoID
FROM ProductCTE p
JOIN ProductProductPhotoCTE ppp ON p.ProductID = ppp.ProductID
WHERE p.ProductModelID BETWEEN 120 AND 130;

SELECT ProductID, ProductName, ProductModelID, PhotoID
FROM @MyTableVar
ORDER BY ProductModelID;
