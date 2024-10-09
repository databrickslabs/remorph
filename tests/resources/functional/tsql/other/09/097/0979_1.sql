--Query type: DDL
SELECT *
INTO #CustomerOrders
FROM (
    VALUES (
        1, 'John Doe', '2022-01-01',
        2, 'Jane Doe', '2022-01-02'
    )
) AS temp_table(order_key, customer_name, order_date);

SELECT *
FROM #CustomerOrders;

-- REMORPH CLEANUP: DROP TABLE #CustomerOrders;