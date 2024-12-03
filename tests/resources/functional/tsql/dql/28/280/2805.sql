--Query type: DQL
SELECT TIMEFROMPARTS(hour_value, minute_value, second_value, 0, 0) AS constructed_time FROM (VALUES (12, 30, 0)) AS time_components (hour_value, minute_value, second_value);
