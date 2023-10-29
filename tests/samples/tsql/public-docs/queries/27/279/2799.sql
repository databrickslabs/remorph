-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/nodes-method-xml-data-type?view=sql-server-ver16

SELECT T2.Loc.query('.')  
FROM T  
CROSS APPLY Instructions.nodes('/root/Location') AS T2(Loc)