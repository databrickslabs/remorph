-- tsql sql:
CREATE TABLE NewTable (ID_Num INT IDENTITY(1,1) PRIMARY KEY);
INSERT INTO NewTable (ID_Num) VALUES (1), (2), (3);
SELECT * FROM NewTable;