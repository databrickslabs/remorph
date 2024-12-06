-- tsql sql:
DECLARE @myVariable INT = 10;
SELECT value
FROM (
    VALUES (@myVariable)
) AS mySubquery(value);
