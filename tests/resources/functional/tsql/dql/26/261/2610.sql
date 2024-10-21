--Query type: DQL
WITH CustomerData AS (
    SELECT 'John' AS CustomerName, 'Doe' AS CustomerLastName
    UNION ALL
    SELECT 'Jane', 'Smith'
)
SELECT FORMATMESSAGE('This is the %s and this is the %s.', CustomerName, CustomerLastName) AS Result
FROM CustomerData;