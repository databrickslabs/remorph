--Query type: DDL
CREATE TABLE #Customer
(
    id INT NOT NULL,
    lastName VARCHAR(20),
    orderCount INT,
    orderDate DATE
);

INSERT INTO #Customer (id, lastName, orderCount, orderDate)
VALUES
    (1, 'Smith', 60, '2022-01-01'),
    (2, 'Johnson', 30, '2021-06-01'),
    (3, 'Williams', 90, '2022-03-01'),
    (4, 'Jones', 10, '2020-09-01'),
    (5, 'Brown', 25, '2021-12-01');

WITH CustomerCTE AS
(
    SELECT
        CASE
            WHEN orderCount > 50 THEN 'High'
            WHEN orderCount BETWEEN 10 AND 50 THEN 'Medium'
            ELSE 'Low'
        END AS orderCategory,
        orderDate,
        orderCount,
        lastName
    FROM #Customer
)

SELECT
    orderCategory,
    SUM(CASE WHEN orderDate > '2020-01-01' THEN 1 ELSE 0 END) AS recentOrders,
    AVG(orderCount) AS averageOrderCount,
    STRING_AGG(lastName, ', ') AS customerNames
FROM CustomerCTE
GROUP BY orderCategory
HAVING AVG(orderCount) > 20
ORDER BY orderCategory DESC;

SELECT * FROM #Customer;

DROP TABLE #Customer;
