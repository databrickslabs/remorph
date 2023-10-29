-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-selective-xml-index-transact-sql?view=sql-server-ver16

CREATE SELECTIVE XML INDEX on T1(C1)  
WITH XMLNAMESPACES ('https://www.tempuri.org/' as myns)  
FOR ( path1 = '/myns:book/myns:author/text()' );