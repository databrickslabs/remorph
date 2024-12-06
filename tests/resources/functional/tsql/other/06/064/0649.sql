-- tsql sql:
WITH temp_result AS ( SELECT n1, CASE WHEN n1 > 100 THEN 1 WHEN n1 > 10 THEN 1 ELSE 0 END AS insert_into_t1 FROM src ) INSERT INTO t1 (n1) SELECT n1 FROM temp_result WHERE insert_into_t1 = 1; INSERT INTO t2 (n1) SELECT n1 FROM temp_result WHERE insert_into_t1 = 0;
