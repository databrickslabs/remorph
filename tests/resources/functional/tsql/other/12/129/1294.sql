-- tsql sql:
WITH stg_DimCustomer AS (
    SELECT 1 AS CustomerKey, 'Customer 1' AS EnglishCustomerName, 'Red' AS Color
    UNION ALL
    SELECT 2 AS CustomerKey, 'Customer 2' AS EnglishCustomerName, 'Blue' AS Color
),
DimCustomer AS (
    SELECT 3 AS CustomerKey, 'Customer 3' AS EnglishCustomerName, 'Green' AS Color
    UNION ALL
    SELECT 4 AS CustomerKey, 'Customer 4' AS EnglishCustomerName, 'Yellow' AS Color
),
DimCustomer_upsert AS (
    SELECT s.CustomerKey, s.EnglishCustomerName, s.Color
    FROM stg_DimCustomer AS s
    UNION ALL
    SELECT c.CustomerKey, c.EnglishCustomerName, c.Color
    FROM DimCustomer AS c
    WHERE NOT EXISTS (
        SELECT *
        FROM stg_DimCustomer s
        WHERE s.CustomerKey = c.CustomerKey
    )
)
SELECT *
FROM DimCustomer_upsert;
