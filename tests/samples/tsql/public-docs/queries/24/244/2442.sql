-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/nodes-method-xml-data-type?view=sql-server-ver16

SELECT C.query('.') as result  
FROM Production.ProductModel  
CROSS APPLY Instructions.nodes('  
declare namespace MI="https://schemas.microsoft.com/sqlserver/2004/07/adventure-works/ProductModelManuInstructions";  
/MI:root/MI:Location') as T(C)  
WHERE ProductModelID=7