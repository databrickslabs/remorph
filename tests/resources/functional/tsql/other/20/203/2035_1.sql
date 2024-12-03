--Query type: DML
WITH temp_table AS (SELECT GETDATE() AS c1, GETDATE() AS c2)
INSERT t2 (c1, c2)
VALUES ((SELECT c1 FROM temp_table), (SELECT c2 FROM temp_table));
