-- tsql sql:
DECLARE @TranName VARCHAR(20);
SELECT @TranName = 'MyTransaction';
BEGIN TRANSACTION @TranName;
CREATE TABLE #Region (
    R_REGIONKEY INT
);
INSERT INTO #Region (
    R_REGIONKEY
)
VALUES (
    1
);
WITH Region AS (
    SELECT *
    FROM #Region
)
DELETE FROM Region
WHERE R_REGIONKEY = 1;
SELECT *
FROM #Region;
COMMIT TRANSACTION @TranName;
DROP TABLE #Region;
-- REMORPH CLEANUP: DROP TABLE #Region;
