--Query type: DML
INSERT INTO #temp_result
SELECT column_a, column_b, [Previous value for column_b] = LAG(column_b) IGNORE NULLS OVER (ORDER BY column_a), [Next value for column_b] = LEAD(column_b) IGNORE NULLS OVER (ORDER BY column_a)
FROM (
    VALUES (1, 8), (2, 9), (3, NULL), (4, 10), (5, NULL), (6, NULL), (7, 11)
) AS data (column_a, column_b)
ORDER BY column_a;
