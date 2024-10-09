--Query type: DDL
CREATE TABLE ext_table_2 (value VARCHAR(50));
INSERT INTO ext_table_2 (value)
VALUES ('value3'), ('value4');
SELECT * FROM ext_table_2;
-- REMORPH CLEANUP: DROP TABLE ext_table_2;