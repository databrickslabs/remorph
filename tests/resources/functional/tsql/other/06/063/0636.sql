--Query type: DDL
CREATE TABLE parent (ID INTEGER);
CREATE TABLE child (ID INTEGER, parent_ID INTEGER);

WITH temp_result AS (
    SELECT 1 AS column1, 'value1' AS column2, 100.00 AS column3
)
SELECT * FROM temp_result;

PRINT 'Completed';

-- REMORPH CLEANUP: DROP TABLE parent;
-- REMORPH CLEANUP: DROP TABLE child;