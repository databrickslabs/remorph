--Query type: DCL
CREATE TABLE #test_table (id INT, name VARCHAR(50));
CREATE ROLE data_reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::dbo TO data_reader;
INSERT INTO #test_table (id, name) VALUES (1, 'Test');
WITH temp_result AS (
    SELECT id, name FROM #test_table
)
SELECT * FROM temp_result;
-- REMORPH CLEANUP: DROP TABLE #test_table;
DROP ROLE data_reader;