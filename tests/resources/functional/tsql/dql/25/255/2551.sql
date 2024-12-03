--Query type: DQL
WITH temp_result AS (SELECT 5 AS num, SYSDATETIME() AS curr_date)
SELECT DATE_BUCKET(WEEK, (num * 2), curr_date)
FROM temp_result;
