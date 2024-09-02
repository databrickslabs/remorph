--Query type: DQL
DECLARE @v1 DATETIME = '2022-01-01';
SELECT @v1 AS [DATE_TIME], CAST(@v1 AS VARCHAR(20)) AS [date time as varchar]
FROM (VALUES (1)) AS T(T);