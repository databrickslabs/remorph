--Query type: DML
CREATE TABLE array_demo (ID INT, array1 VARCHAR(255), array2 VARCHAR(255), tip VARCHAR(255));
INSERT INTO array_demo (ID, array1, array2, tip)
VALUES (1, '1,2,3', '3,4,5', 'value 1'),
      (2, '1,2,3', '3,4,5', 'value 3 overlaps');
SELECT *
FROM array_demo;
-- REMORPH CLEANUP: DROP TABLE array_demo;
