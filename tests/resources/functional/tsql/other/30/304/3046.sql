--Query type: DML
CREATE TABLE MyTitles (id INT, name VARCHAR(50));
INSERT INTO MyTitles (id, name) VALUES (101, 'MyTitle');
WITH MyCTE AS (
    SELECT name
    FROM MyTitles
    WHERE id = 101
)
UPDATE MyCTE
SET name = 'ADifferentName';
SELECT *
FROM MyTitles;
-- REMORPH CLEANUP: DROP TABLE MyTitles;
