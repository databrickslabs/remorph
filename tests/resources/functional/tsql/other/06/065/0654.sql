--Query type: DML
CREATE TABLE array_test (ID INT, array1 VARCHAR(MAX), array2 VARCHAR(MAX));

WITH temp_result AS (
    SELECT 1 AS ID, '1,2,3' AS array1, '4,5,6' AS array2
)
INSERT INTO array_test (ID, array1, array2)
SELECT ID, array1, array2
FROM temp_result;

SELECT * FROM array_test;