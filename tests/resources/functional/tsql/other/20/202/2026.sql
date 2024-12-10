-- tsql sql:
WITH CustomerCTE AS (
    SELECT id, lastName, orderCount, orderDate
    FROM (
        VALUES (1, 'Smith', 5, '2020-01-01'),
               (2, 'Johnson', 10, '2020-01-15'),
               (3, 'Williams', 20, '2020-02-01')
    ) AS Customer(id, lastName, orderCount, orderDate)
)
SELECT id, lastName, orderCount, orderDate
FROM CustomerCTE;
