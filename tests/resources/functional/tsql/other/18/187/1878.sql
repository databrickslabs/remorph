-- tsql sql:
DECLARE @number INT;
SET @number = 10;
SELECT *
FROM (
    VALUES (@number)
) AS temp_result (result);
