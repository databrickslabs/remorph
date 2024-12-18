-- tsql sql:
DECLARE @i INT = 0;
BEGIN TRANSACTION;
SET @i = 0;
WHILE (@i < 100000)
BEGIN
    INSERT INTO T1 (id, str)
    SELECT num, CAST(num AS CHAR(3))
    FROM (VALUES (@i)) AS Numbers(num);
    SET @i += 1;
END;
COMMIT TRANSACTION;
