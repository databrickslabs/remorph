--Query type: DQL
WITH temp_result AS (SELECT 'Returns the length.' AS input_string)
SELECT dbo.new_udf(input_string)
FROM temp_result
