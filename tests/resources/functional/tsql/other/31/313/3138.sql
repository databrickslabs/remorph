-- tsql sql:
DECLARE @MyVariable INT;
SET @MyVariable = 1;
SELECT MyVariable
FROM (
    VALUES (@MyVariable)
) AS MyCTE (MyVariable);
