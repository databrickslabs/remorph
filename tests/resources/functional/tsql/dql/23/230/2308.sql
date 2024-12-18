-- tsql sql:
WITH temp_result AS (SELECT 'The number of degrees in PI/2 radians is: ' AS message, DEGREES((PI()/2)) AS degrees)
SELECT message + CONVERT(VARCHAR, degrees) AS result
FROM temp_result
