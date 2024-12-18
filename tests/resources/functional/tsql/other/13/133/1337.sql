-- tsql sql:
WITH temp_result AS (
    SELECT 1 AS o_orderkey, NULL AS o_custkey, 'O' AS o_orderstatus, 10.00 AS o_totalprice, '2022-01-01' AS o_orderdate, 'HIGH' AS o_orderpriority, 'John' AS o_clerk, 1 AS o_shippriority, 'Comment' AS o_comment
)
SELECT *
INTO orders
FROM temp_result;

ALTER TABLE orders
ADD CONSTRAINT UC_orders UNIQUE (o_orderkey, o_custkey);

SELECT *
FROM orders;
