--Query type: DQL
DECLARE @MyValue VARCHAR(10) = 'safety';
WITH DocumentCTE AS (
  SELECT DocumentSummary, DocumentNode
  FROM (
    VALUES ('DocumentSummary1', 0x7B40),
           ('DocumentSummary2', 0x7B41)
  ) AS Document (DocumentSummary, DocumentNode)
)
SELECT position = PATINDEX('%' + @MyValue + '%', DocumentSummary)
FROM DocumentCTE
WHERE DocumentNode = 0x7B40;