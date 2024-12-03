--Query type: DQL
WITH cte AS (SELECT GETDATE() AS currentDateTime)
SELECT TODATETIMEOFFSET(currentDateTime, '-07:00') AS offsetDateTime
FROM cte
