-- tsql sql:
CREATE TABLE array_test (ID INT, array1 VARCHAR(MAX), array2 VARCHAR(MAX), tip VARCHAR(MAX));
WITH temp_result AS (
    SELECT 1 AS ID, '5,6,7,8' AS array1, '7,8,9' AS array2, 'values 7 and 8 overlap' AS tip
)
INSERT INTO array_test (ID, array1, array2, tip)
SELECT * FROM temp_result;
SELECT * FROM array_test;
-- REMORPH CLEANUP: DROP TABLE array_test;
