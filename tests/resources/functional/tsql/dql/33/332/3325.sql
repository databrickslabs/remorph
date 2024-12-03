--Query type: DQL
SELECT AVG(CASE o_orderpriority WHEN 'HIGH' THEN 1 WHEN 'MEDIUM' THEN 2 WHEN 'LOW' THEN 3 ELSE 5 END) AS average_order_priority FROM (VALUES (1, 'HIGH'), (2, 'MEDIUM'), (3, NULL)) AS orders (o_orderkey, o_orderpriority);
