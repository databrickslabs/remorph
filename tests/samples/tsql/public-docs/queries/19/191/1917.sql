-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/exist-method-xml-data-type?view=sql-server-ver16

DECLARE @x XML;  
DECLARE @f BIT;  
SET @x = '<Somedate>2002-01-01Z</Somedate>';  
SET @f = @x.exist('/Somedate[(text()[1] cast as xs:date ?) = xs:date("2002-01-01Z") ]')  
SELECT @f;