--Query type: DML
CREATE TABLE test_table (phone_number VARCHAR(20) DEFAULT '123-456-7890');
INSERT INTO test_table (phone_number)
VALUES ('123-456-7890');
SELECT *
FROM test_table;
-- REMORPH CLEANUP: DROP TABLE test_table;