--Query type: DML
DECLARE @LocNumber INT;
SET @LocNumber = NEXT VALUE FOR Test.CountBy1;
INSERT INTO #NewLocation (LocNumber, Name)
SELECT @LocNumber, Name
FROM (
    VALUES ('Location1'),
           ('Location2'),
           ('Location3')
) AS LocationCTE (Name);
SELECT *
FROM #NewLocation;
-- Create table #NewLocation (LocNumber INT, Name VARCHAR(50));
-- REMORPH CLEANUP: DROP TABLE #NewLocation;