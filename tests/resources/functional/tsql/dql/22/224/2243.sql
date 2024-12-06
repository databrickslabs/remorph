-- tsql sql:
WITH SalesRank AS (
    SELECT region, nation, SUM(revenue) AS total_revenue, RANK() OVER (PARTITION BY region ORDER BY SUM(revenue) DESC) AS revenue_rank
    FROM (
        VALUES ('North', 'USA', 100.0),
               ('North', 'Canada', 200.0),
               ('South', 'Brazil', 300.0),
               ('South', 'Argentina', 400.0)
    ) AS Sales (region, nation, revenue)
    GROUP BY region, nation
)
SELECT region, nation, total_revenue, revenue_rank
FROM SalesRank
ORDER BY region, revenue_rank;
