--Query type: DML
CREATE TABLE TableA (id INT, value INT);
CREATE TABLE TableB (id INT, value INT);

INSERT INTO TableA (id, value)
VALUES (1, 10), (2, 20);

INSERT INTO TableB (id, value)
VALUES (1, 30), (2, 40), (3, 50);

SELECT * FROM TableA;
SELECT * FROM TableB;

-- REMORPH CLEANUP: DROP TABLE TableB;
-- REMORPH CLEANUP: DROP TABLE TableA;
