--Query type: DQL
WITH temp_result AS (SELECT 2.0 AS value)
SELECT POWER(CAST(value AS FLOAT), -100.0) AS FloatResult,
       POWER(2, -100.0) AS IntegerResult,
       POWER(CAST(value AS INT), -100.0) AS IntegerResult,
       POWER(value, -100.0) AS Decimal1Result,
       POWER(2.00, -100.0) AS Decimal2Result,
       POWER(CAST(value AS DECIMAL(5,2)), -100.0) AS Decimal2Result
FROM temp_result