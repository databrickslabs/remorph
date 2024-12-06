-- tsql sql:
CREATE TABLE TempTable (ID INT);
INSERT INTO TempTable VALUES (1);
DENY SELECT ON TempTable TO [Customer];
SELECT * FROM TempTable;
-- REMORPH CLEANUP: DROP TABLE TempTable;
