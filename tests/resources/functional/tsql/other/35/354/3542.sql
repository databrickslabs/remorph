--Query type: DCL
CREATE TABLE #MyTable (id INT);
INSERT INTO #MyTable (id)
VALUES
    (1),
    (2),
    (3);

WITH MyCTE AS (
SELECT id
FROM #MyTable
)
SELECT *
FROM MyCTE;

SELECT *
FROM (
VALUES
    (1),
    (2),
    (3)
) AS MyTable (id);

-- REMORPH CLEANUP: DROP TABLE #MyTable;