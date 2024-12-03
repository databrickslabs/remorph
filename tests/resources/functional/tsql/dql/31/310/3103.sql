--Query type: DQL
WITH CustomerAddress AS (
    SELECT 'New York' AS City, 'customer1@example.com' AS EmailAddress
    UNION ALL
    SELECT 'Los Angeles', 'customer2@example.com'
)
SELECT TOP 10
    City,
    STRING_AGG(CONVERT(NVARCHAR(max), EmailAddress), ';') AS emails
FROM CustomerAddress
GROUP BY City;
