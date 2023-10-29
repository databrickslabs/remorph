-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/remserver-transact-sql?view=sql-server-ver16

CREATE PROCEDURE usp_CheckServer  
AS  
SELECT @@REMSERVER;