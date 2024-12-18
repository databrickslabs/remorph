-- tsql sql:
WITH temp AS (SELECT 'Hello' + ' ' + 'World' + ' is a string.' AS result)
SELECT result
FROM temp;
