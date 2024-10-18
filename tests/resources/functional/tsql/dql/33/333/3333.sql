--Query type: DQL
SELECT COUNT(*) AS TotalCount
FROM (
    VALUES (1), (2), (3)
) AS Customer (C_CustomerKey);