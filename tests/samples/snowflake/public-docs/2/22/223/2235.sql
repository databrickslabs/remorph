SELECT
    column1,
    column2,
    NTH_VALUE(column2, 2) OVER (PARTITION BY column1 ORDER BY column2) AS column2_2nd
FROM VALUES
    (1, 10), (1, 11), (1, 12),
    (2, 20), (2, 21), (2, 22);
