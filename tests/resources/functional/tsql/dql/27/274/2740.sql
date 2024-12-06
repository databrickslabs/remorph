-- tsql sql:
WITH T1 AS (
    SELECT n + 10 * m AS powRef
    FROM (
        VALUES (0), (1), (2), (3), (4), (5), (6), (7), (8), (9)
    ) ones(n),
    (
        VALUES (0), (1), (2), (3), (4), (5), (6), (7), (8), (9)
    ) tens(m)
),
T2 AS (
    SELECT POWER(powRef, 2) AS binRef, powRef
    FROM T1
),
T3 AS (
    SELECT (optRef & binRef) / binRef AS flagRef, RIGHT(CONVERT(VARCHAR(2), CAST(powRef AS VARBINARY(1)), 2), 1) AS posRef, CAST((optRef & binRef) / binRef AS INT) AS flagCheck
    FROM T2
    CROSS JOIN (
        VALUES (12345)
    ) f3(optRef)
),
T4 AS (
    SELECT MAX(flagCheck) AS flagCheck, posRef
    FROM T3
    GROUP BY posRef
),
T5 AS (
    SELECT [0], [1], [2], [3], [4], [5], [6], [7], [8], [9]
    FROM (
        SELECT posRef, flagCheck
        FROM T4
    ) P
    PIVOT(
        MAX(flagCheck)
        FOR posRef IN ([0], [1], [2], [3], [4], [5], [6], [7], [8], [9])
    ) P
),
T6 AS (
    SELECT CONCAT('', [0], [1], [2], [3], [4], [5], [6], [7], [8], [9]) AS stib, CONCAT('', [9], [8], [7], [6], [5], [4], [3], [2], [1], [0]) AS Bits
    FROM T5
)
SELECT T6.Bits, CAST(T5.[0] AS BIT) AS [DISABLE_DEF_CNST_CHK], CAST(T5.[1] AS BIT) AS [IMPLICIT_TRANSACTIONS], CAST(T5.[2] AS BIT) AS [CURSOR_CLOSE_ON_COMMIT], CAST(T5.[3] AS BIT) AS [ANSI_WARNINGS], CAST(T5.[4] AS BIT) AS [ANSI_PADDING], CAST(T5.[5] AS BIT) AS [ANSI_NULLS], CAST(T5.[6] AS BIT) AS [ARITHABORT], CAST(T5.[7] AS BIT) AS [ARITHIGNORE], CAST(T5.[8] AS BIT) AS [QUOTED_IDENTIFIER], CAST(T5.[9] AS BIT) AS [NOCOUNT]
FROM T6
CROSS JOIN T5
