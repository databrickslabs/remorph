--Query type: DML
WITH ExistingRecord AS (
    SELECT 1 AS RecordID, 'Existing Record' AS RecordName
),
NonExistentRecord AS (
    SELECT RecordID, RecordName
    FROM ExistingRecord
    WHERE RecordID = 2
)
SELECT *
FROM NonExistentRecord
IF NOT EXISTS (
    SELECT 1
    FROM NonExistentRecord
)
BEGIN
    THROW 51000, 'The record does not exist.', 1;
END