--Query type: DQL
SELECT CONVERT(DATETIME2(0), '2022-10-30T03:01:00', 126) AT TIME ZONE 'Central European Standard Time' AS converted_date
FROM (
    VALUES (1), (2), (3)
) AS temp_result_set(id);