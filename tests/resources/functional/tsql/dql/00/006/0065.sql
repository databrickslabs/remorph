--Query type: DQL
WITH temp_result AS (
    SELECT region,
           SUM(CASE WHEN quarter = 1 THEN sales END) AS Q1,
           SUM(CASE WHEN quarter = 2 THEN sales END) AS Q2,
           SUM(CASE WHEN quarter = 3 THEN sales END) AS Q3,
           SUM(CASE WHEN quarter = 4 THEN sales END) AS Q4
    FROM (
        VALUES ('North', 1, 100),
               ('North', 2, 200),
               ('North', 3, 300),
               ('North', 4, 400),
               ('South', 1, 500),
               ('South', 2, 600),
               ('South', 3, 700),
               ('South', 4, 800)
    ) AS sales(region, quarter, sales)
    GROUP BY region
)
SELECT region, sales, quarter
FROM temp_result
UNPIVOT(sales FOR quarter IN (Q1, Q2, Q3, Q4)) AS unpivoted_sales
ORDER BY region;
