--Query type: DQL
WITH CustomerCTE AS (
    SELECT 'New York' AS City, 'customer1@example.com' AS EmailAddress
    UNION ALL
    SELECT 'Los Angeles', 'customer2@example.com'
    UNION ALL
    SELECT 'Chicago', 'customer3@example.com'
),
SupplierCTE AS (
    SELECT 'New York' AS City, 'supplier1@example.com' AS EmailAddress
    UNION ALL
    SELECT 'Los Angeles', 'supplier2@example.com'
    UNION ALL
    SELECT 'Chicago', 'supplier3@example.com'
)
SELECT TOP 10
    T1.City,
    STRING_AGG(CONVERT(NVARCHAR(max), T2.EmailAddress), ';') WITHIN GROUP (ORDER BY T2.EmailAddress ASC) AS Emails
FROM (
    VALUES ('New York'), ('Los Angeles'), ('Chicago')
) AS T1 (City)
INNER JOIN CustomerCTE AS T2 ON T1.City = T2.City
INNER JOIN SupplierCTE AS T3 ON T2.City = T3.City
GROUP BY T1.City;
