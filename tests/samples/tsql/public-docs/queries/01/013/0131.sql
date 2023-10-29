-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/textsize-transact-sql?view=sql-server-ver16

-- Set the TEXTSIZE option to the default size of 4096 bytes.  
SET TEXTSIZE 0  
SELECT @@TEXTSIZE AS 'Text Size'  
SET TEXTSIZE 2048  
SELECT @@TEXTSIZE AS 'Text Size'