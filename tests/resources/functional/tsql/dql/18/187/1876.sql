--Query type: DQL
DECLARE @orderdate DATE = '1995-01-01';
DECLARE @shipdate DATE = '1995-01-15';

WITH dates AS (
    SELECT @orderdate AS orderdate, @shipdate AS shipdate
)

SELECT DATEDIFF(day, orderdate, shipdate) AS days_diff
FROM dates;