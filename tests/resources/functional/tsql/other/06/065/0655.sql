-- tsql sql:
CREATE TABLE array_test (ID INT, array1 VARCHAR(MAX), array2 VARCHAR(MAX));

WITH temp_result AS (
    SELECT 1 AS ID, '20,30,40' AS array1, '50,60' AS array2
)
INSERT INTO array_test (ID, array1, array2)
SELECT ID, array1, array2
FROM temp_result;

SELECT * FROM array_test;
