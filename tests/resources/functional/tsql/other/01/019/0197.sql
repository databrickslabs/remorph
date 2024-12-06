-- tsql sql:
BEGIN TRANSACTION;
CREATE TABLE #temp_leased
(
    id INT,
    name VARCHAR(10)
);
CREATE TABLE #temp_returned
(
    id INT
);
INSERT INTO #temp_leased (id, name)
VALUES
    (1, 'a'),
    (2, 'b'),
    (3, 'c');
INSERT INTO #temp_returned (id)
VALUES
    (1),
    (2);
DELETE FROM #temp_leased
WHERE id IN (SELECT id FROM #temp_returned);
TRUNCATE TABLE #temp_returned;
COMMIT TRANSACTION;
SELECT * FROM #temp_leased;
-- REMORPH CLEANUP: DROP TABLE #temp_leased;
-- REMORPH CLEANUP: DROP TABLE #temp_returned;
