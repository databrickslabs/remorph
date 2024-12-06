-- tsql sql:
DECLARE @notastring INT;
SET @notastring = 1;
DECLARE @notastring2 INT;
SET @notastring2 = 2;
SELECT *
FROM (
    VALUES (
        CONVERT(VARCHAR(10), @notastring) + ' is not a string.',
        CONVERT(VARCHAR(10), @notastring2) + ' is also not a string.'
    )
) AS temp_result (result, result2);
