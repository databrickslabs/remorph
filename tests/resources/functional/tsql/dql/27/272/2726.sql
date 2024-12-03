--Query type: DQL
SELECT RADIANS(1e-307) AS radian_value FROM (VALUES (1e-307)) AS temp_table(angle_value);
