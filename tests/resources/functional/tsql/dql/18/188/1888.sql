--Query type: DQL
DECLARE @time_var TIME = '14:20:40.456';
SELECT DATEPART(HOUR, @time_var) AS hour_part
FROM (
    VALUES (1)
) AS temp_result_set(id);