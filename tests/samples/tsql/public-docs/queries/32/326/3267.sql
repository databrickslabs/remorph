-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/binary-checksum-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
CREATE TABLE myTable (column1 INT, column2 VARCHAR(256));  
GO  
INSERT INTO myTable VALUES (1, 'test');  
GO  
SELECT BINARY_CHECKSUM(*) from myTable;  
GO  
UPDATE myTable set column2 = 'TEST';  
GO  
SELECT BINARY_CHECKSUM(*) from myTable;  
GO