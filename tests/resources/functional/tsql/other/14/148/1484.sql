--Query type: DML
DECLARE @MyNumber INT;
SET @MyNumber = 4 - 2 + 27;
SELECT Number
FROM (
    VALUES (@MyNumber)
) AS Result (Number);