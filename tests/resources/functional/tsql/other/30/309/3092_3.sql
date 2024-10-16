--Query type: DML
DECLARE @TableVar TABLE (ID INT, Name VARCHAR(10));

WITH TempResult AS (
    SELECT 1 AS ID, 'Test' AS Name
    UNION ALL
    SELECT 2 AS ID, 'Demo' AS Name
)

INSERT INTO @TableVar (ID, Name)
SELECT ID, Name
FROM TempResult;

IF @@ROWCOUNT = 0
    PRINT 'Warning: No rows were inserted into @TableVar';
ELSE
    PRINT 'Rows inserted into @TableVar: ' + CONVERT(VARCHAR, @@ROWCOUNT);

SELECT *
FROM @TableVar;

-- REMORPH CLEANUP: DROP TABLE @TableVar;