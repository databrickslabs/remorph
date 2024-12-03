--Query type: DQL
SELECT CONCAT('Order ', o_orderkey, ' was placed on ', o_orderdate) AS OrderInfo FROM (VALUES (1, '2022-01-01'), (2, '2022-01-15'), (3, '2022-02-01')) AS Orders(o_orderkey, o_orderdate);
