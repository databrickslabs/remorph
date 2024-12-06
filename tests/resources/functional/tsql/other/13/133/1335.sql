-- tsql sql:
CREATE TABLE t2 (c1 INT, c2 TEXT);
EXEC sp_tableoption 't2', 'text in row', 'on';
INSERT INTO t2
SELECT *
FROM (
    VALUES (1, 'This is text.')
) AS tv (c1, c2);
