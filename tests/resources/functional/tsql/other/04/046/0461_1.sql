-- tsql sql:
DECLARE @NewBalance INT;
SET @NewBalance = 10;
SET @NewBalance *= 10;
WITH NewCTE AS (
    SELECT @NewBalance AS NewBalance
)
SELECT TOP 1 *, (
    SELECT COUNT(*)
    FROM sys.views
) AS ViewCount
FROM NewCTE;
