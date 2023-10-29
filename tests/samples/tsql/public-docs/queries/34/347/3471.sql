-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/insert-xml-dml?view=sql-server-ver16

USE AdventureWorks;  
GO  
DECLARE @myDoc XML;  
SET @myDoc = '<Root>  
<ProductDescription ProductID="1" ProductName="Road Bike">  
<Features>  
  
</Features>  
</ProductDescription>  
</Root>'  
SELECT @myDoc;  
SET @myDoc.modify('  
 insert text{"Product Catalog Description"}   
 as first into (/Root)[1]  
');  
SELECT @myDoc;