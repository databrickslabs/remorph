--Query type: DDL
CREATE TABLE #et2
(
    column1 INT,
    column2 NVARCHAR(50),
    location NVARCHAR(50)
);

INSERT INTO #et2 (column1, column2, location)
VALUES
    (1, 'value1', '2022/01'),
    (2, 'value2', '2022/02'),
    (3, 'value3', '2022/03');

DECLARE @location NVARCHAR(50);

WITH temp_table AS (SELECT '2022/01' AS location)
SELECT @location = location FROM temp_table;

DELETE FROM #et2 WHERE location = @location;

SELECT * FROM #et2;

DROP TABLE #et2;
-- REMORPH CLEANUP: DROP TABLE #et2;
