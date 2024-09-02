--Query type: DML
INSERT INTO #temp_result (column_a, column_b, [Previous value for column_b], [Next value for column_b])
SELECT column_a, column_b, [Previous value for column_b], [Next value for column_b]
FROM (
    SELECT column_a, column_b, [Previous value for column_b] = LAG(column_b) OVER (ORDER BY column_a) WITH (RESPECT NULLS), [Next value for column_b] = LEAD(column_b) OVER (ORDER BY column_a) WITH (RESPECT NULLS)
    FROM (
        VALUES (1, 8), (2, 9), (3, NULL), (4, 10), (5, NULL), (6, NULL), (7, 11)
    ) AS v(column_a, column_b)
) AS result
ORDER BY column_a;