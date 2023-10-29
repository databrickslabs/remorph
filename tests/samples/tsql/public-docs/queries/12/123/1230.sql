-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16

CREATE TABLE T1 (
  C1 INT PRIMARY KEY,
  C2 VARCHAR(50) SPARSE NULL,
  C3 INT SPARSE NULL,
  C4 INT) ;
GO