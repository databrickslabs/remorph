--Query type: DML
CREATE TABLE sname_example (id INT, name VARCHAR(50));
INSERT INTO sname_example DEFAULT VALUES;
SELECT * FROM (VALUES ('default')) AS temp_table(column_name);
SELECT * FROM sname_example;
-- REMORPH CLEANUP: DROP TABLE sname_example;
