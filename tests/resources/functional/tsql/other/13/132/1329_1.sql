--Query type: DDL
WITH temp_result AS (
    SELECT c1, c2
    FROM (
        VALUES (1, 10), (2, 20), (3, 30), (4, 40), (5, 50)
    ) AS temp(c1, c2)
)
SELECT c1, c2, COUNT(c1) OVER (PARTITION BY c2) AS cnt,
    LAG(c1, 1, 0) OVER (PARTITION BY c2 ORDER BY c1) AS prev_c1,
    LEAD(c1, 1, 0) OVER (PARTITION BY c2 ORDER BY c1) AS next_c1,
    ROW_NUMBER() OVER (PARTITION BY c2 ORDER BY c1) AS row_num,
    RANK() OVER (PARTITION BY c2 ORDER BY c1) AS rank,
    DENSE_RANK() OVER (PARTITION BY c2 ORDER BY c1) AS dense_rank,
    NTILE(2) OVER (PARTITION BY c2 ORDER BY c1) AS ntile,
    PERCENT_RANK() OVER (PARTITION BY c2 ORDER BY c1) AS percent_rank,
    CUME_DIST() OVER (PARTITION BY c2 ORDER BY c1) AS cume_dist
FROM temp_result
WHERE c1 > 0
ORDER BY c1, c2
OFFSET 1 ROW
FETCH NEXT 10 ROW ONLY;
