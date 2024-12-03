--Query type: DML
CREATE TABLE MyTempTable (col1 INT PRIMARY KEY);
INSERT INTO MyTempTable
SELECT *
FROM (
    VALUES (1),
    (2),
    (3)
) AS MyTempTable (col1);

WITH MyCTE AS (
    SELECT *
    FROM (
        VALUES (1),
        (2),
        (3)
    ) AS MyTempTable (col1)
)
SELECT *
FROM MyCTE;

-- REMORPH CLEANUP: DROP TABLE MyTempTable;
