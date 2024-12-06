-- tsql sql:
DECLARE @x4 INT = 54;
SET @x4 /= 3;
SELECT *
FROM (
    VALUES (@x4)
) AS temp_result (Divided_by_3);
