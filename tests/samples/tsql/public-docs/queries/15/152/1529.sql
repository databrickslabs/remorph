-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/rand-transact-sql?view=sql-server-ver16

DECLARE @counter SMALLINT;

SET @counter = 1;

WHILE @counter < 5
BEGIN
    SELECT RAND() Random_Number
    SET @counter = @counter + 1
END;
GO