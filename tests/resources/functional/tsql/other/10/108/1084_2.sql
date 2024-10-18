--Query type: DDL
WITH CustomerOrders AS (
    SELECT c_custkey,
           SUM(o_totalprice) AS total_order_value,
           AVG(o_totalprice) AS avg_order_value,
           ROW_NUMBER() OVER (ORDER BY SUM(o_totalprice) DESC) AS row_num,
           RANK() OVER (ORDER BY SUM(o_totalprice) DESC) AS rank_value
    FROM (
        VALUES (1, 1, 100.0),
               (2, 2, 200.0),
               (3, 3, 50.0),
               (1, 1, 150.0),
               (2, 2, 250.0)
    ) AS Orders(o_orderkey, o_custkey, o_totalprice)
    INNER JOIN (
        VALUES (1, 1),
               (2, 2),
               (3, 3),
               (4, 1),
               (5, 2)
    ) AS Customer(o_custkey, c_custkey)
        ON Orders.o_custkey = Customer.o_custkey
    GROUP BY c_custkey
),
     RankedCustomers AS (
    SELECT c_custkey,
           total_order_value,
           avg_order_value,
           row_num,
           rank_value,
           CASE
               WHEN rank_value <= 2 THEN 'High Value'
               ELSE 'Low Value'
           END AS customer_category
    FROM CustomerOrders
)
SELECT rc.c_custkey,
       rc.total_order_value,
       rc.avg_order_value,
       rc.row_num,
       rc.rank_value,
       rc.customer_category,
       COALESCE(SUM(so_totalprice), 0) AS supplier_order_total
FROM RankedCustomers rc
LEFT JOIN (
    VALUES (1, 1000.0),
           (2, 2000.0),
           (3, 500.0)
) AS SupplierOrders(so_suppkey, so_totalprice)
    ON rc.c_custkey = SupplierOrders.so_suppkey
GROUP BY rc.c_custkey,
         rc.total_order_value,
         rc.avg_order_value,
         rc.row_num,
         rc.rank_value,
         rc.customer_category
ORDER BY rc.total_order_value DESC;