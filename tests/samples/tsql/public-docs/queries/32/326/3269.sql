-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/col-length-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
CREATE TABLE t1(c1 VARCHAR(40), c2 NVARCHAR(40) );  
GO  
SELECT COL_LENGTH('t1','c1')AS 'VarChar',  
      COL_LENGTH('t1','c2')AS 'NVarChar';  
GO  
DROP TABLE t1;