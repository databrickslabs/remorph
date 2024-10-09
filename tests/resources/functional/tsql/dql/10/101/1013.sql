--Query type: DQL
WITH temp_result AS (SELECT 15 AS input_value)
SELECT dbo.ConvertInput(TR1.input_value) AS 'ConvertedValue'
FROM temp_result TR1;