-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/add-transact-sql?view=sql-server-ver16

SET NOCOUNT ON  
DECLARE @startdate DATETIME, @adddays INT;  
SET @startdate = 'January 10, 1900 12:00 AM';  
SET @adddays = 5;  
SET NOCOUNT OFF;  
SELECT @startdate + 1.25 AS 'Start Date',   
   @startdate + @adddays AS 'Add Date';