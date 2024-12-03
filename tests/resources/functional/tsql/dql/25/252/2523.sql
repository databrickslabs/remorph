--Query type: DQL
SELECT DATEADD(month, (SELECT TOP 1 l_orderkey FROM (VALUES (1, '2022-01-01'), (2, '2022-01-15'), (3, '2022-02-01')) AS orders (l_orderkey, o_orderdate)), (SELECT MAX(o_orderdate) FROM (VALUES (1, '2022-01-01'), (2, '2022-01-15'), (3, '2022-02-01')) AS orders (l_orderkey, o_orderdate)))
