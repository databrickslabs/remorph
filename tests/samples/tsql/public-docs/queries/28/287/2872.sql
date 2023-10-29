-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/value-method-xml-data-type?view=sql-server-ver16

SELECT c1, c2, c3   
FROM T  
WHERE c3.exist( '/root[@a=sql:column("c1")]') = 1  
GO