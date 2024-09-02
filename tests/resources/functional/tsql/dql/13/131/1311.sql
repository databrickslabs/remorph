--Query type: DQL
WITH datetimeoffset_values AS (
    SELECT CAST('2022-01-01 12:00:00.0000000 +02:00' AS datetimeoffset) AS ColDatetimeoffset
)
SELECT SWITCHOFFSET(ColDatetimeoffset, '-08:00') AS result
FROM datetimeoffset_values;