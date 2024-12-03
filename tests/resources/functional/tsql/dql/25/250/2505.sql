--Query type: DQL
WITH TempResult AS ( SELECT l_orderkey, l_extendedprice FROM lineitem ) SELECT l_orderkey, l_extendedprice FROM TempResult GROUP BY l_orderkey, l_extendedprice
