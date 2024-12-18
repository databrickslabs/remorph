-- tsql sql:
DECLARE @SearchTerm NVARCHAR(30);
SET @SearchTerm = N'customer';

WITH CustomerComments AS (
    SELECT 'The customer is very satisfied with the product.' AS Comment
    UNION ALL
    SELECT 'The customer had some issues with the delivery.' AS Comment
)

SELECT Comment
FROM CustomerComments
WHERE Comment LIKE '%' + @SearchTerm + '%';
