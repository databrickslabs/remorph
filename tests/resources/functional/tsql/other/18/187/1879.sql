--Query type: DML
DECLARE @number INT;
SET @number = 10;
SELECT @number + ' is a number.' AS Result
FROM (
    VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10)
) AS Numbers(Num)
WHERE Num <= @number;