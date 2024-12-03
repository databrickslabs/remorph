--Query type: DML
CREATE TABLE t1 (a INT, b INT, c AS a / b); INSERT INTO t1 (a, b) SELECT a, b FROM (VALUES (1, 2), (3, 4)) AS v (a, b);
