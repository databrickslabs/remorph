-- tsql sql:
DECLARE @value INT, @counter INT;
SET @value = 2;
SET @counter = 1;

WHILE @counter < 5
BEGIN
    SELECT POWER(@value, @counter) AS result
    FROM (VALUES (1)) AS temp(value);

    SET NOCOUNT ON;
    SET @counter = @counter + 1;
    SET NOCOUNT OFF;
END;
