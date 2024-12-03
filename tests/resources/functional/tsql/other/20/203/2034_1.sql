--Query type: DML
WITH temp_result AS ( SELECT id, value FROM ( VALUES (1, 8), (2, 9), (3, NULL), (4, 10), (5, NULL), (6, NULL), (7, 11) ) AS temp (id, value) ) INSERT INTO test_ignore_nulls (id, value) SELECT id, value FROM temp_result
