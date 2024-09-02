--Query type: DDL
CREATE TABLE #temp_result (id INT, name VARCHAR(10));
INSERT INTO #temp_result (id, name)
VALUES (1, 'a'), (2, 'b'), (3, 'c');
CREATE INDEX idx_temp_result ON #temp_result (id) WITH (ONLINE = ON);
DROP INDEX idx_temp_result ON #temp_result WITH (ONLINE = ON, MOVE TO NewGroup);
SELECT * FROM #temp_result;
-- REMORPH CLEANUP: DROP TABLE #temp_result;