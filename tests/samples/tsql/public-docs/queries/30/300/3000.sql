-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datefirst-transact-sql?view=sql-server-ver16

SET DATEFIRST 5;  
SELECT @@DATEFIRST AS 'First Day'  
    ,DATEPART(dw, SYSDATETIME()) AS 'Today';