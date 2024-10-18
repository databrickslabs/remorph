--Query type: DQL
WITH ProductDescription AS (
    SELECT 'High-performance products for the modern world' AS Description
    UNION ALL
    SELECT 'Ergonomic design for comfort and style'
    UNION ALL
    SELECT 'Innovative technology for the future'
)
SELECT Description
FROM ProductDescription
WHERE Description LIKE '%high-performance%';