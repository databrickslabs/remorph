--Query type: DQL
WITH CustomerData AS (
    SELECT customer_id, customer_name
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2')
    ) AS Customer(customer_id, customer_name)
)
SELECT DB_NAME(customer_id) AS [Customer],
       customer_id
FROM CustomerData;
