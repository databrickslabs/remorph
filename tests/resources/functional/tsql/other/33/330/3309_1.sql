--Query type: DML
WITH TempResult AS (
    SELECT 'John' AS FirstName, 'Doe' AS LastName
    UNION ALL
    SELECT 'Jane', 'Smith'
    UNION ALL
    SELECT 'Bob', 'Johnson'
)
SELECT IDENTITY(smallint, 100, 1) AS ContactNum, FirstName AS First, LastName AS Last
INTO #NewContact
FROM TempResult;

SELECT *
FROM #NewContact;

-- REMORPH CLEANUP: DROP TABLE #NewContact;
