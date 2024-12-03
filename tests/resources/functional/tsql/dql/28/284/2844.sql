--Query type: DQL
SELECT VARP(T1.extendedprice) AS variance_extendedprice FROM (VALUES (1, 10.0), (2, 20.0), (3, 30.0)) AS T1 (orderid, extendedprice);
