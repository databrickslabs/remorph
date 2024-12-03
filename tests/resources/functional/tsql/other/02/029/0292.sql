--Query type: DML
CREATE TABLE array_demo (ID INT, array1 VARCHAR(MAX), array2 VARCHAR(MAX), tip VARCHAR(MAX));
WITH temp_result AS (
    SELECT 1 AS ID, '1,2' AS array1, '3,4' AS array2, 'non-overlapping' AS tip
)
INSERT INTO array_demo (ID, array1, array2, tip)
SELECT * FROM temp_result;
SELECT * FROM array_demo;
-- REMORPH CLEANUP: DROP TABLE array_demo;
