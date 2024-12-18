-- tsql sql:
CREATE TABLE #Document
(
    DocumentID INT,
    DocumentSummary VARCHAR(MAX),
    Title NVARCHAR(50)
);

INSERT INTO #Document
(
    DocumentID,
    DocumentSummary,
    Title
)
VALUES
(
    1,
    'This is a document summary.',
    N'Crank Arm and Tire Maintenance'
),
(
    2,
    'This is another document summary.',
    N'Other Title'
);

WITH DocumentCTE AS
(
    SELECT DocumentID, DocumentSummary, Title
    FROM #Document
)
UPDATE DocumentCTE
SET DocumentSummary = DocumentSummary.WRITE('', 9, 12)
WHERE Title = N'Crank Arm and Tire Maintenance';

SELECT *
FROM #Document;
-- REMORPH CLEANUP: DROP TABLE #Document;
