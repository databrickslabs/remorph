--Query type: DQL
DECLARE @new_angle FLOAT;
SET @new_angle = 0.1234567;
WITH temp_table AS (
    SELECT 1 AS temp_column
)
SELECT 'The ASIN of the new angle is: ' + CONVERT(VARCHAR, ASIN(@new_angle)) AS result
FROM temp_table;