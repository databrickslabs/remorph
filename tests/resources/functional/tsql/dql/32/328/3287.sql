-- tsql sql:
DECLARE @SearchWord VARCHAR(30);
SET @SearchWord = 'performance';

WITH ProductDescriptions AS (
    SELECT 'This is a high-performance product.' AS Description
    UNION ALL
    SELECT 'This product is not related to performance.'
)

SELECT Description
FROM ProductDescriptions
WHERE Description LIKE '%' + @SearchWord + '%';
