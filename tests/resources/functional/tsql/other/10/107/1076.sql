--Query type: DML
CREATE TABLE myTable (col1 INT, col2 VARCHAR(50));
INSERT INTO myTable (col1, col2)
VALUES
    (1, 'a row'),
    (100, 'another row'),
    (500, 'another row'),
    (1000, 'another row');
SELECT * FROM myTable;
-- REMORPH CLEANUP: DROP TABLE myTable;