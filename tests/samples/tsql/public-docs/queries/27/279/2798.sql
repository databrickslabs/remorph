-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/nodes-method-xml-data-type?view=sql-server-ver16

SELECT T.c.query('..') AS result  
FROM   @x.nodes('/Root/row') T(c)  
GO