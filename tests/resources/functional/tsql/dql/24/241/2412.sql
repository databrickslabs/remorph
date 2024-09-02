--Query type: DQL
WITH temp_result AS (SELECT 'A' AS char1, 'B' AS char2, 'a' AS char3, 'b' AS char4, 1 AS num1, 2 AS num2)
SELECT ASCII(char1) AS char1_ascii, ASCII(char2) AS char2_ascii, ASCII(char3) AS char3_ascii, ASCII(char4) AS char4_ascii, ASCII(num1) AS num1_ascii, ASCII(num2) AS num2_ascii
FROM temp_result