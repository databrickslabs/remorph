--Query type: DDL
WITH T1 AS (
    SELECT Col1, Col2
    FROM (
        VALUES (1, 'abc'),
               (2, 'def')
    ) AS T (Col1, Col2)
),
T2 AS (
    SELECT Col3, Col4
    FROM (
        VALUES (10, 20),
               (30, 40)
    ) AS T (Col3, Col4)
)
SELECT
    CASE
        WHEN T1.Col1 > 10 THEN 'Greater than 10'
        WHEN T1.Col1 = 10 THEN 'Equal to 10'
        ELSE 'Less than 10'
    END AS Result,
    IIF (T1.Col1 > 10, 'Greater than 10', 'Less than or equal to 10') AS Result2,
    T1.Col1 + T2.Col3 AS SumResult,
    T1.Col1 * T2.Col3 AS MultiplyResult,
    T1.Col1 / T2.Col3 AS DivideResult,
    T1.Col1 % T2.Col3 AS ModulusResult,
    POWER (T1.Col1, T2.Col3) AS PowerResult,
    FLOOR (T1.Col1) AS FloorResult,
    CEILING (T1.Col1) AS CeilingResult,
    ROUND (T1.Col1, 2) AS RoundResult,
    CONVERT (VARCHAR(10), T1.Col1) AS ConvertResult,
    CAST (T1.Col1 AS VARCHAR(10)) AS CastResult,
    ISNULL (T1.Col1, 0) AS IsNullResult,
    COALESCE (T1.Col1, T2.Col3, 0) AS CoalesceResult,
    LTRIM (RTRIM (T1.Col2)) AS TrimResult,
    LEN (T1.Col2) AS LengthResult,
    LOWER (T1.Col2) AS LowerResult,
    UPPER (T1.Col2) AS UpperResult,
    REPLACE (T1.Col2, 'a', 'b') AS ReplaceResult,
    SUBSTRING (T1.Col2, 2, 3) AS SubstringResult,
    CHARINDEX ('a', T1.Col2) AS CharIndexResult,
    PATINDEX ('%a%', T1.Col2) AS PatIndexResult,
    REVERSE (T1.Col2) AS ReverseResult,
    STUFF (T1.Col2, 2, 3, 'abc') AS StuffResult,
    SPACE (10) AS SpaceResult,
    STR (10, 5, 2) AS StrResult,
    LEN (T1.Col2) AS TextLenResult,
    GETDATE () AS GetDateResult,
    DATEADD (day, 10, GETDATE ()) AS DateAddResult,
    DATEDIFF (day, GETDATE (), DATEADD (day, 10, GETDATE ())) AS DateDiffResult,
    DATENAME (month, GETDATE ()) AS DateNameResult,
    DATEPART (month, GETDATE ()) AS DatePartResult,
    DAY (GETDATE ()) AS DayResult,
    MONTH (GETDATE ()) AS MonthResult,
    YEAR (GETDATE ()) AS YearResult,
    ISDATE ('2022-01-01') AS IsDateResult,
    ISNULL (T1.Col1, 0) + ISNULL (T2.Col3, 0) AS IsNullSumResult
FROM T1
CROSS JOIN T2