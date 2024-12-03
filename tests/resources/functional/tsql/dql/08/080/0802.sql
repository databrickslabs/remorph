--Query type: DQL
SELECT 'Text for ' + CONVERT(VARCHAR(10), o_orderpriority) + ' is ' + CONVERT(VARCHAR(10), o_totalprice) AS result FROM (VALUES (1, 100.0), (2, 200.0), (3, 300.0)) AS orders(o_orderpriority, o_totalprice);
