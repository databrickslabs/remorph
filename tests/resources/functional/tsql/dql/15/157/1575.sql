--Query type: DQL
DECLARE @datetimeoffset datetimeoffset(4) = '2022-12-10 12:32:10 +01:00';
SELECT
    datetimeoffset,
    CAST(datetimeoffset AS date) AS 'date'
FROM (
    VALUES (@datetimeoffset)
) AS tempTable(datetimeoffset);