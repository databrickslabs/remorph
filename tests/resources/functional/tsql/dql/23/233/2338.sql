--Query type: DQL
SELECT *
FROM (
    SELECT '1' AS c1, '2' AS c2, '3' AS c3
    UNION ALL
    SELECT '4', '5', '6'
) AS T1
INNER JOIN (
    SELECT '1' AS c1, '2' AS c2, '3' AS c3
    UNION ALL
    SELECT '4', '5', '6'
) AS T2
ON T1.c1 = T2.c1;
