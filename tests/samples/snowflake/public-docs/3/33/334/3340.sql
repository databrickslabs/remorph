CREATE TABLE table1 (i int);
BEGIN TRANSACTION;
INSERT INTO table1 (i) VALUES (1);
INSERT INTO table1 (i) VALUES ('This is not a valid integer.');    -- FAILS!
INSERT INTO table1 (i) VALUES (2);
COMMIT;
SELECT i FROM table1 ORDER BY i;