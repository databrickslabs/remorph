-- tsql sql:
DECLARE @result INT;
SET @result = (SELECT value FROM (VALUES (27)) AS temp_result(value));
SET @result ^= 2;
SELECT @result AS Bitwise_Exclusive_OR;
