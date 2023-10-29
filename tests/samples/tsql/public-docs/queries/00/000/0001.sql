-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/like-transact-sql?view=sql-server-ver16

-- ASCII pattern matching with char column
CREATE TABLE t (col1 CHAR(30));

INSERT INTO t
VALUES ('Robert King');

SELECT * FROM t
WHERE col1 LIKE '% King'; -- returns 1 row

-- Unicode pattern matching with nchar column
CREATE TABLE t (col1 NCHAR(30));

INSERT INTO t
VALUES ('Robert King');

SELECT * FROM t
WHERE col1 LIKE '% King'; -- no rows returned

-- Unicode pattern matching with nchar column and RTRIM
CREATE TABLE t (col1 NCHAR(30));

INSERT INTO t
VALUES ('Robert King');

SELECT * FROM t
WHERE RTRIM(col1) LIKE '% King'; -- returns 1 row