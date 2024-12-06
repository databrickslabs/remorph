-- tsql sql:
SETUSER 'mary';
WITH orders AS (
    SELECT '1-URGENT' AS o_orderpriority, 1000 AS o_totalprice, '1992-01-01' AS o_orderdate
    UNION ALL
    SELECT '2-HIGH', 2000, '1992-01-02'
    UNION ALL
    SELECT '3-MEDIUM', 3000, '1992-01-03'
    UNION ALL
    SELECT '4-NOT SPECIFIED', 4000, '1992-01-04'
    UNION ALL
    SELECT '5-LOW', 5000, '1992-01-05'
)
SELECT
    SUM(CASE WHEN o_orderpriority = '1-URGENT' THEN 1 ELSE 0 END) AS priority_urgent,
    SUM(CASE WHEN o_orderpriority = '2-HIGH' THEN 1 ELSE 0 END) AS priority_high,
    SUM(CASE WHEN o_orderpriority = '3-MEDIUM' THEN 1 ELSE 0 END) AS priority_medium,
    SUM(CASE WHEN o_orderpriority = '4-NOT SPECIFIED' THEN 1 ELSE 0 END) AS priority_not_specified,
    SUM(CASE WHEN o_orderpriority = '5-LOW' THEN 1 ELSE 0 END) AS priority_low
FROM orders
WHERE o_orderdate >= '1992-01-01' AND o_orderdate < '1993-01-01'
ORDER BY priority_urgent DESC;
