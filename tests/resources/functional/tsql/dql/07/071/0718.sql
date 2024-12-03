--Query type: DQL
WITH temp_result AS (
    SELECT 'description1' AS description, '2022-01-01 12:00:00' AS value
    UNION ALL
    SELECT 'description2' AS description, '2022-01-02 13:00:00' AS value
)
SELECT description, value, CONVERT(datetime, value) AS timestamp_value, CONVERT(time, value) AS time_value
FROM temp_result
ORDER BY value;
