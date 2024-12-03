--Query type: DML
WITH XMLData AS (
  SELECT CONVERT(XML, '<Root>
<ProductDescription ProductID="1" ProductName="Road Bike">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>') AS myDoc
)
SELECT
  myDoc.value('(/Root/ProductDescription/@ProductID)[1]', 'int') AS ProdID
FROM XMLData;
-- REMORPH CLEANUP: DROP TABLE XMLData;
