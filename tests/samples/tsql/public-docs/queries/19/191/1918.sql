-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/exist-method-xml-data-type?view=sql-server-ver16

DECLARE @x XML;  
DECLARE @f BIT;  
SET @x = '<root Somedate = "2002-01-01Z"/>';  
SET @f = @x.exist('/root[(@Somedate cast as xs:date?) eq xs:date("2002-01-01Z")]');  
SELECT @f;