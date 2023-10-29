-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-xml-schema-collection-transact-sql?view=sql-server-ver16

CREATE FUNCTION dbo.MyFunction()  
RETURNS int  
WITH SCHEMABINDING  
AS  
BEGIN  
   /* some code may go here */
   DECLARE @x XML(MyCollection)  
   /* more code may go here */
END;