-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-index-transact-sql?view=sql-server-ver16

CREATE TABLE t1 (a INT, b INT, c AS a/b);
INSERT INTO t1 VALUES (1, 0);