--Query type: DML
CREATE TABLE #Tool
(
    ToolID INT IDENTITY(1, 1),
    ToolName VARCHAR(50)
);

SET IDENTITY_INSERT #Tool ON;

WITH Tool AS
(
    SELECT 1 AS ToolID, 'Tool1' AS ToolName
    UNION ALL
    SELECT 2, 'Tool2'
)
INSERT INTO #Tool (ToolID, ToolName)
SELECT ToolID, ToolName
FROM Tool;

SET IDENTITY_INSERT #Tool OFF;

SELECT *
FROM #Tool;