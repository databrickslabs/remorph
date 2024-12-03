--Query type: DDL
WITH TempResult AS (
    SELECT 'John' AS FirstName, 'Doe' AS LastName, '123 Main St' AS Address
    UNION ALL
    SELECT 'Jane', 'Doe', '456 Elm St'
)
SELECT
    FirstName,
    LastName,
    Address
INTO #TempTable
FROM TempResult;

ALTER TABLE #TempTable
ALTER COLUMN FirstName VARCHAR(50) NOT NULL;
ALTER TABLE #TempTable
ALTER COLUMN LastName VARCHAR(50) NOT NULL;
ALTER TABLE #TempTable
ALTER COLUMN Address VARCHAR(100) NOT NULL;

CREATE UNIQUE NONCLUSTERED INDEX UX_TempTable_FirstName ON #TempTable (FirstName);

ALTER TABLE #TempTable
ADD CONSTRAINT CK_TempTable_FirstName CHECK (FirstName <> '');
ALTER TABLE #TempTable
ADD CONSTRAINT CK_TempTable_LastName CHECK (LastName <> '');
ALTER TABLE #TempTable
ADD CONSTRAINT CK_TempTable_Address CHECK (Address <> '');
