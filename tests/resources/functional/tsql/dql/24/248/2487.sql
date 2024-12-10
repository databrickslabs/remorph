-- tsql sql:
WITH temp_result AS (SELECT 14.76 AS value1, -0.1472738 AS value2)
SELECT COS(value1) AS cosCalc1, COS(value2) AS cosCalc2
FROM temp_result
