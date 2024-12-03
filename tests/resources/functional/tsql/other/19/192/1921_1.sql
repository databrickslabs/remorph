--Query type: DCL
WITH temp_result AS (SELECT CONVERT(date, '2022-01-01') AS date_column)
SELECT FORMAT(date_column, 'd', 'en-gb') AS formatted_date
FROM temp_result;
