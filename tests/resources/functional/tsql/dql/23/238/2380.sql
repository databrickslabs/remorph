--Query type: DQL
SELECT (c1 * c2) / (c3 + c4) AS Result1, (c5 * c6) / (c7 + c8) AS Result2
FROM (
    VALUES
        (10, 20, 3, 4, 100, 200, 30, 40),
        (1000, 2000, 300, 400, 10000, 20000, 3000, 4000)
) AS T (c1, c2, c3, c4, c5, c6, c7, c8);