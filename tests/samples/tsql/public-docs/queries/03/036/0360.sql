-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/subtract-transact-sql?view=sql-server-ver16

-- Uses the AdventureWorks sample database
DECLARE @altstartdate DATETIME;  
SET @altstartdate = CONVERT(DATETIME, 'January 10, 1900 3:00 AM', 101);  
SELECT @altstartdate - 1.5 AS 'Subtract Date';