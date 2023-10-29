-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/exist-method-xml-data-type?view=sql-server-ver16

DECLARE @x XML;  
SET @x='';  
SELECT @x.exist('true()');