--Query type: DQL
DECLARE @angle FLOAT;
SET @angle = 0.5;
SELECT 'The ASIN of the angle is: ' + CONVERT(VARCHAR, ASIN(@angle))
FROM (VALUES (1)) AS temp_result(column_name);
