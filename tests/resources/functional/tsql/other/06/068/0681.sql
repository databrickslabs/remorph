--Query type: DML
CREATE TABLE objects_3 (id INT, object3 VARCHAR(MAX), variant3 VARCHAR(MAX));

WITH cte AS (
    SELECT 1 AS id, '{"g": 7, "h": 8, "i": 9}' AS object3, '{"g": 7, "h": 8, "i": 9}' AS variant3
)
INSERT INTO objects_3 (id, object3, variant3)
SELECT id, object3, variant3
FROM cte;

SELECT * FROM objects_3;

-- REMORPH CLEANUP: DROP TABLE objects_3;