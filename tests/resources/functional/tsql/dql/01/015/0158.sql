--Query type: DQL
DECLARE @time_in_ny datetimeoffset = '2018-04-05 12:00:00 +02:00';
DECLARE @tz_ny nvarchar(50) = 'Eastern Standard Time';
DECLARE @tz_la nvarchar(50) = 'Pacific Standard Time';

WITH time_zones AS (
    SELECT @tz_ny AS tz_name, @time_in_ny AS time_in_ny
    UNION ALL
    SELECT @tz_la, @time_in_ny
)

SELECT tz.tz_name, tz.time_in_ny AT TIME ZONE tz.tz_name AS time_in_la
FROM time_zones tz;
