-- tsql sql:
DECLARE @angle FLOAT;
SET @angle = 0.5;
SELECT 'The ASIN of the angle is: ' + CONVERT(VARCHAR, ASIN(@angle))
FROM (VALUES (@angle)) AS temp_result(angle);
