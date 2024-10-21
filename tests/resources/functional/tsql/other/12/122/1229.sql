--Query type: DDL
CREATE TABLE T2 (d int, e int NULL, f varchar(20));
INSERT INTO T2 (d, e, f)
VALUES (1, 2, 'test');
SELECT * FROM T2;
-- REMORPH CLEANUP: DROP TABLE T2;