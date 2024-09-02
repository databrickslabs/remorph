--Query type: DQL
WITH p AS (SELECT 100 AS value)
SELECT Distance * (SELECT value FROM p) AS [Distance * value]
FROM (VALUES ('USA', 1000), ('Canada', 2000)) AS Region (Country, Distance);