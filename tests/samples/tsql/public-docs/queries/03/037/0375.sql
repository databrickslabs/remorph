-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/identity-function-transact-sql?view=sql-server-ver16

--(1)  
SELECT IDENTITY(int, 1,1) AS ID_Num  
INTO NewTable  
FROM OldTable;  
  
--(2)  
SELECT ID_Num = IDENTITY(int, 1, 1)  
INTO NewTable  
FROM OldTable;