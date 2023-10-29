-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/isjson-transact-sql?view=sql-server-ver16

SELECT id, json_col
FROM tab1
WHERE ISJSON(json_col, SCALAR) = 1