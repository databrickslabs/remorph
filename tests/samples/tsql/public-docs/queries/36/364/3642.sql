-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/with-common-table-expression-transact-sql?view=sql-server-ver16

WITH DirectReports(Name, Title, EmployeeID, EmployeeLevel, Sort)
AS (SELECT CONVERT(VARCHAR(255), e.FirstName + ' ' + e.LastName),
        e.Title,
        e.EmployeeID,
        1,
        CONVERT(VARCHAR(255), e.FirstName + ' ' + e.LastName)
    FROM dbo.MyEmployees AS e
    WHERE e.ManagerID IS NULL
    UNION ALL
    SELECT CONVERT(VARCHAR(255), REPLICATE ('|    ' , EmployeeLevel) +
        e.FirstName + ' ' + e.LastName),
        e.Title,
        e.EmployeeID,
        EmployeeLevel + 1,
        CONVERT (VARCHAR(255), RTRIM(Sort) + '|    ' + FirstName + ' ' +
                 LastName)
    FROM dbo.MyEmployees AS e
    JOIN DirectReports AS d ON e.ManagerID = d.EmployeeID
    )
SELECT EmployeeID, Name, Title, EmployeeLevel
FROM DirectReports
ORDER BY Sort;