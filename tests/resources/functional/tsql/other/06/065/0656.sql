--Query type: DML
CREATE TABLE array_demo_3 (ID INT, array1 INT, array2 INT);
WITH temp_result AS (
    SELECT 1 AS ID, 2 AS array1, 4 AS array2
)
INSERT INTO array_demo_3 (ID, array1, array2)
SELECT ID, array1, array2
FROM temp_result;
SELECT * FROM array_demo_3;
-- REMORPH CLEANUP: DROP TABLE array_demo_3;