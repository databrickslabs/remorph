--Query type: DDL
CREATE TABLE t2 (c3 datetimeoffset(7), c4 smalldatetime, c5 float);
INSERT INTO t2 (c3, c4, c5)
SELECT CAST('2022-01-01 12:00:00 +02:00' AS datetimeoffset(7)), CAST('2022-01-01 12:00:00' AS smalldatetime), CAST(10.5 AS float);
SELECT * FROM t2;
-- REMORPH CLEANUP: DROP TABLE t2;