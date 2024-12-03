--Query type: DQL
WITH temp_result AS (SELECT 11 AS num1, 11 AS num2, -11 AS num3, 50 AS num4, -50 AS num5)
SELECT FORMATMESSAGE('Unsigned hexadecimal %x, %X, %X, %x', num1, num2, num3, num4, num5)
FROM temp_result
