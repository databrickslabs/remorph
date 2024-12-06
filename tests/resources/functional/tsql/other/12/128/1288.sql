-- tsql sql:
CREATE TABLE dbo.T1 (Col1 INT, Col2 CHAR(3));
INSERT INTO dbo.T1
SELECT *
FROM (VALUES (1, 'abc')) AS T2 (Col1, Col2);
