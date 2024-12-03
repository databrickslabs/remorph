--Query type: DML
DECLARE @NewBalance INT;
SET @NewBalance = 10;
SET @NewBalance = @NewBalance * 10;
WITH TempResult AS (
    SELECT @NewBalance AS FinalBalance
)
SELECT * FROM TempResult;
