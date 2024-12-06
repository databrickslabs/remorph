-- tsql sql:
DECLARE @SearchTerm NVARCHAR(30);
SET @SearchTerm = N'Quality';

WITH TempResult AS (
    SELECT 'High quality products' AS ProductInfo
    UNION ALL
    SELECT 'Good quality products' AS ProductInfo
)

SELECT ProductInfo
FROM TempResult
WHERE ProductInfo LIKE '%' + @SearchTerm + '%';
