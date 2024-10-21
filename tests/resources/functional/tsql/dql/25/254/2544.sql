--Query type: DQL
WITH DateParts AS (
    SELECT 2015 AS Year, 1 AS Month, 1 AS Day, 0 AS Hour, 0 AS Minute, 0 AS Second, 0 AS Millisecond
)
SELECT DATETIMEFROMPARTS(Year, Month, Day, Hour, Minute, Second, Millisecond) AS Result
FROM DateParts;