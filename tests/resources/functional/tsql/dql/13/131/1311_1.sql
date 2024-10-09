--Query type: DQL
WITH temp_result AS (SELECT CAST('2022-01-01 12:00:00.0000000 +00:00' AS DATETIMEOFFSET) AS ColDatetimeoffset)
SELECT ColDatetimeoffset
FROM temp_result;