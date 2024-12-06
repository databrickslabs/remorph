-- tsql sql:
DECLARE @MyTableVar TABLE (NewScrapReasonID smallint, Name varchar(50), ModifiedDate datetime);
INSERT INTO Production.ScrapReason (Name, ModifiedDate)
OUTPUT INSERTED.ScrapReasonID, INSERTED.Name, INSERTED.ModifiedDate
INTO @MyTableVar
VALUES (N'Operator error', GETDATE());
SELECT * FROM @MyTableVar;
-- REMORPH CLEANUP: DROP TABLE @MyTableVar;
