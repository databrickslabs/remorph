--Query type: DML
DECLARE @counter SMALLINT;
SET @counter = 1;

WHILE @counter < 5
BEGIN
    SELECT RAND() AS Random_Number
    FROM (
        VALUES (1), (2), (3), (4)
    ) AS temp_result(counter);

    SET @counter = @counter + 1;
END;