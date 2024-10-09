--Query type: DQL
WITH EmployeeCTE AS (
    SELECT 'Smith' AS LastName, 'John' AS FirstName
    UNION ALL
    SELECT 'Johnson', 'Mike'
    UNION ALL
    SELECT 'Williams', 'David'
)
SELECT UPPER(RTRIM(LastName)) + ', ' + FirstName AS Name
FROM EmployeeCTE
ORDER BY LastName;