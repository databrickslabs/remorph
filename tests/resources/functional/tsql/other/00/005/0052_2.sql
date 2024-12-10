-- tsql sql:
CREATE TABLE new_target (k INT, v INT);
INSERT INTO new_target (k, v)
VALUES (1, 1), (2, 2), (3, 3);
MERGE INTO new_target AS T
USING (VALUES (1, 1001), (2, 500), (3, 2000)) AS S (o_custkey, o_totalprice)
ON T.k = S.o_custkey
WHEN MATCHED AND S.o_totalprice > 1000
THEN UPDATE SET T.v = S.o_totalprice;
SELECT * FROM new_target;
-- REMORPH CLEANUP: DROP TABLE new_target;
