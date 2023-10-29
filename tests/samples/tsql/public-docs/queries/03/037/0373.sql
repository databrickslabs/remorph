-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/insert-xml-dml?view=sql-server-ver16

-- check the update  
SELECT x.query(' //ProductDescription/Features')  
FROM T;  
GO