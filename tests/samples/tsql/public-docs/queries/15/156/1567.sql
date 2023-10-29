-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/datetime-transact-sql?view=sql-server-ver16

DECLARE @date date = '2016-12-21';  
DECLARE @datetime datetime = @date;  

SELECT @datetime AS '@datetime', @date AS '@date';