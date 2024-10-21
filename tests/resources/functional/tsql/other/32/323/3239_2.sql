--Query type: DML
CREATE TABLE #DocumentCTE
(
    DocumentID INT,
    Title NVARCHAR(50),
    DocumentSummary NVARCHAR(100)
);

INSERT INTO #DocumentCTE
(
    DocumentID,
    Title,
    DocumentSummary
)
VALUES
(
    1,
    N'Crank Arm and Tire Maintenance',
    N'Summary 1'
),
(
    2,
    N'Chain and Sprocket Maintenance',
    N'Summary 2'
),
(
    3,
    N'Brake Pad Maintenance',
    N'Summary 3'
);

UPDATE #DocumentCTE
SET DocumentSummary = DocumentSummary + N' updated'
WHERE Title = N'Crank Arm and Tire Maintenance';

SELECT *
FROM #DocumentCTE;
-- REMORPH CLEANUP: DROP TABLE #DocumentCTE;