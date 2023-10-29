-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

DECLARE @myval DECIMAL(5, 2);
SET @myval = 193.57;

SELECT CAST(CAST(@myval AS VARBINARY(20)) AS DECIMAL(10, 5));

-- Or, using CONVERT
SELECT CONVERT(DECIMAL(10, 5), CONVERT(VARBINARY(20), @myval));
GO