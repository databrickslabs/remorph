--Query type: DQL
DECLARE @myval DECIMAL(5, 2);
SET @myval = 193.57;

WITH myvalues AS (
    SELECT CAST(CAST(@myval AS VARBINARY(20)) AS DECIMAL(10, 5)) AS val1,
           CONVERT(DECIMAL(10, 5), CONVERT(VARBINARY(20), @myval)) AS val2
)
SELECT val1, val2
FROM myvalues
