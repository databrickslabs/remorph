--Query type: DQL
SELECT AVG(l_extendedprice) AS [Average Price]
FROM (
    VALUES (17.00), (10.00), (23.00), (9.00), (1.00)
) AS tpc_h_lineitem(l_extendedprice);