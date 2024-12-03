--Query type: DQL
DECLARE @o_orderdate DATE = '11/22/2020';
WITH orders AS (
    SELECT 1 AS o_orderkey, @o_orderdate AS o_orderdate
)
SELECT FORMAT(o.o_orderdate, 'd', 'en-US') AS 'US English',
       FORMAT(o.o_orderdate, 'd', 'en-gb') AS 'British English',
       FORMAT(o.o_orderdate, 'd', 'de-de') AS 'German',
       FORMAT(o.o_orderdate, 'd', 'zh-cn') AS 'Chinese Simplified (PRC)'
FROM orders o;
