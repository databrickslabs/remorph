--Query type: DQL
SELECT c_name, o_orderkey FROM ( VALUES ('Customer#000000001', 1), ('Customer#000000002', 2), ('Customer#000000003', 3) ) AS c (c_name, c_custkey) LEFT OUTER HASH JOIN ( VALUES (1, 1), (2, 2), (3, 3) ) AS o (o_orderkey, o_custkey) ON c.c_custkey = o.o_custkey ORDER BY o_orderkey DESC;
