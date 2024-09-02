--Query type: DDL
CREATE TABLE discount_levels (discount_level VARCHAR(20));
WITH lineitem AS (
    SELECT 0.05 AS l_discount
    UNION ALL
    SELECT 0.15
    UNION ALL
    SELECT 0.05
    UNION ALL
    SELECT 0.15
    UNION ALL
    SELECT 0.05
)
INSERT INTO discount_levels
SELECT CASE
        WHEN SUM(CASE WHEN l_discount > 0.1 THEN 1 ELSE 0 END) > SUM(CASE WHEN l_discount < 0.1 THEN 1 ELSE 0 END) THEN 'High Discount'
        ELSE 'Low Discount'
    END AS discount_level
FROM lineitem