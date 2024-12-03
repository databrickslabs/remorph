--Query type: DQL
WITH datetime_cte AS (SELECT SYSDATETIME() AS current_datetime)
SELECT TODATETIMEOFFSET(current_datetime, '+13:00') AS datetime_offset
FROM datetime_cte
