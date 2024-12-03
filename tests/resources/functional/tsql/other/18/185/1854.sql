--Query type: DML
DECLARE @counter INT;
CREATE TABLE #temp_result (c1 INT);
SET @counter = 1;
WHILE (@counter < 101)
BEGIN
    INSERT INTO #temp_result (c1)
    VALUES (1);
    UPDATE #temp_result
    SET c1 = 1
    WHERE c1 = 1;
    SELECT @counter = @counter + 1;
END;
SELECT * FROM #temp_result;
-- REMORPH CLEANUP: DROP TABLE #temp_result;
