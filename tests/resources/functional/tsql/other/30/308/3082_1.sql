--Query type: DML
CREATE TABLE ScrapReason
(
    NewScrapReasonID SMALLINT,
    Name VARCHAR(50),
    ModifiedDate DATETIME
);

WITH MySubquery AS
(
    SELECT 1 AS NewScrapReasonID, N'Operator error' AS Name, GETDATE() AS ModifiedDate
)
INSERT INTO ScrapReason (NewScrapReasonID, Name, ModifiedDate)
OUTPUT INSERTED.NewScrapReasonID, INSERTED.Name, INSERTED.ModifiedDate
SELECT NewScrapReasonID, Name, ModifiedDate
FROM MySubquery;

SELECT * FROM ScrapReason;
-- REMORPH CLEANUP: DROP TABLE ScrapReason;