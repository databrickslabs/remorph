--Query type: DQL
WITH SalesCTE AS (
    SELECT region, SUM(sales) AS total_sales, AVG(sales) AS avg_sales, MAX(sales) AS max_sales, MIN(sales) AS min_sales
    FROM (
        VALUES ('North', 100), ('South', 200), ('East', 300), ('West', 400)
    ) AS Sales(region, sales)
    GROUP BY region
),
CustomerCTE AS (
    SELECT customer_id, region, SUM(order_total) AS total_orders
    FROM (
        VALUES (1, 'North', 1000), (2, 'South', 2000), (3, 'East', 3000), (4, 'West', 4000)
    ) AS Customer(customer_id, region, order_total)
    GROUP BY customer_id, region
)
SELECT s.region, s.total_sales, c.customer_id, c.total_orders
FROM SalesCTE s
INNER JOIN CustomerCTE c ON s.region = c.region
WHERE s.total_sales > (
    SELECT AVG(total_sales)
    FROM SalesCTE
) AND c.total_orders > 2000
GROUP BY s.region, s.total_sales, c.customer_id, c.total_orders
HAVING s.total_sales > 500
