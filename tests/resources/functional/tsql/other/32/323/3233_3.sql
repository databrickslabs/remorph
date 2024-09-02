--Query type: DML
SELECT *
INTO #Tools
FROM (
    VALUES (1, 'Hammer'),
           (2, 'Saw'),
           (3, 'Drill')
) AS ToolCTE (
    ToolID,
    Name
);

DELETE FROM #Tools
WHERE Name = 'Saw';

SELECT *
FROM #Tools;
-- REMORPH CLEANUP: DROP TABLE #Tools;