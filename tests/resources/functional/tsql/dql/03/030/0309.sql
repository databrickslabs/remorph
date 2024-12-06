-- tsql sql:
WITH EmployeeCTE AS (
    SELECT '1992-01-01' AS HireDate
    UNION ALL
    SELECT '1993-01-01'
    UNION ALL
    SELECT '1994-01-01'
),
DateRangeCTE AS (
    SELECT MIN(HireDate) AS MinDate, MAX(HireDate) AS MaxDate
    FROM EmployeeCTE
)
SELECT TOP(1) DATEDIFF(day, MinDate, MaxDate) AS DateDiff
FROM DateRangeCTE
