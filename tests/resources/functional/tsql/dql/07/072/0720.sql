--Query type: DQL
WITH temp_result AS (
    SELECT c_custkey, c_nation, o_orderkey, o_totalprice, LAG(o_totalprice) OVER (ORDER BY o_orderkey) AS prev_order_total
    FROM (
        VALUES (1, 'USA', 1, 100.0),
               (2, 'Canada', 2, 200.0),
               (3, 'Mexico', 3, 300.0)
    ) AS orders (c_custkey, c_nation, o_orderkey, o_totalprice)
)
SELECT c_custkey, c_nation, o_orderkey, o_totalprice,
       CASE
           WHEN o_totalprice = prev_order_total THEN 'No Change'
           WHEN prev_order_total IS NULL THEN 'New Order'
           ELSE 'Changed'
       END AS order_total_changes
FROM temp_result;