--Query type: DML
CREATE TABLE new_target_orig (k INT, v INT);
INSERT INTO new_target_orig (k, v)
VALUES (1, 10), (2, 20);
CREATE TABLE new_src (k INT, v INT);
INSERT INTO new_src (k, v)
VALUES (1, 11), (2, 22);
DROP TABLE IF EXISTS new_target;
SELECT *
INTO new_target
FROM new_target_orig;
MERGE INTO new_target AS T
USING (SELECT k, v FROM new_src) AS S
ON T.k = S.k
WHEN MATCHED AND S.v = 11 THEN DELETE
WHEN MATCHED THEN UPDATE SET T.v = S.v;
SELECT *
FROM new_target;
-- REMORPH CLEANUP: DROP TABLE new_target;
-- REMORPH CLEANUP: DROP TABLE new_target_orig;
-- REMORPH CLEANUP: DROP TABLE new_src;