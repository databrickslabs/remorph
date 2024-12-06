-- tsql sql:
CREATE TABLE T4 ( C1 INT PRIMARY KEY, C2 VARCHAR(50) NULL, C3 INT NULL, C4 INT ); SELECT * FROM ( VALUES (1, 'Value1', 10, 20), (2, 'Value2', 20, 30), (3, 'Value3', 30, 40) ) AS TempResult (C1, C2, C3, C4);
