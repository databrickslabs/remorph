--Query type: DML
INSERT INTO t2 (a) SELECT a FROM (VALUES (NULL)) AS temp(a);