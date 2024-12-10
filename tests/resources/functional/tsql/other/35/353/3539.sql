-- tsql sql:
SELECT o_orderpriority, o_extendedprice, o_orderdate FROM ( VALUES ('1-URGENT', 10.0, '1993-07-01', 1), ('2-HIGH', 20.0, '1993-08-01', 2), ('3-MEDIUM', 30.0, '1993-09-01', 3) ) AS orders (o_orderpriority, o_extendedprice, o_orderdate, o_orderkey) WHERE o_orderdate >= '1993-07-01' AND o_orderdate < '1993-10-01' ORDER BY o_extendedprice DESC
