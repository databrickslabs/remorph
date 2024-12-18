-- tsql sql:
DECLARE @myvariable INT;
SET @myvariable = 5;
SELECT *
FROM (
    VALUES (@myvariable + 10)
) AS temp_result(result);
