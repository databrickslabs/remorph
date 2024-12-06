-- tsql sql:
CREATE TABLE temp_result (id INT, name VARCHAR(50));
INSERT INTO temp_result (id, name)
VALUES (1, 'John'), (2, 'Jane');
GRANT SELECT ON temp_result TO public;
SELECT * FROM temp_result;
-- REMORPH CLEANUP: DROP TABLE temp_result;
