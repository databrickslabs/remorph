-- tsql sql:
WITH customer AS (SELECT 1 AS custkey, 'Customer1' AS name, 1 AS nationkey), orders AS (SELECT 1 AS custkey, 1000000 AS totalprice) SELECT c.custkey, c.name, SUM(o.totalprice) AS total FROM customer c INNER JOIN orders o ON c.custkey = o.custkey WHERE c.nationkey = 1 GROUP BY c.custkey, c.name HAVING SUM(o.totalprice) > 1000000 ORDER BY total DESC
