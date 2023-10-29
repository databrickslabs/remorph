-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/insert-xml-dml?view=sql-server-ver16

USE AdventureWorks;  
GO  
DECLARE @myDoc XML;             
SET @myDoc =   
'<Root>             
    <ProductDescription ProductID="1" ProductName="Road Bike">             
        <Features> </Features>             
    </ProductDescription>             
</Root>' ;            
SELECT @myDoc ;            
SET @myDoc.modify('             
insert <![CDATA[ <notxml> as text </notxml> or cdata ]]>   
into  (/Root/ProductDescription/Features)[1] ') ;   
SELECT @myDoc ;  
GO