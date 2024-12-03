--Query type: DQL
SELECT STDEV(DISTINCT o_totalprice) AS Distinct_Values, STDEV(o_totalprice) AS All_Values FROM (VALUES (1, 100.0), (2, 200.0), (3, 300.0), (4, 400.0), (5, 500.0)) AS orders (o_orderkey, o_totalprice);
