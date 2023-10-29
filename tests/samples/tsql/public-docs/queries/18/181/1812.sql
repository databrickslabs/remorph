-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/binding-relational-data-inside-xml-data?view=sql-server-ver16

DECLARE @isbn VARCHAR(20)  
SET     @isbn = '0-7356-1588-2'  
SELECT  xCol  
FROM    T  
WHERE   xCol.exist ('/book/@ISBN[. = sql:variable("@isbn")]') = 1