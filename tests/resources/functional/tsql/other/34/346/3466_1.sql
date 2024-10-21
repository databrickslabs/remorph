--Query type: DML
INSERT INTO T (ProductID, ProductName, ProductDescription)
SELECT ProductID, ProductName, ProductDescription
FROM (
    VALUES
        (1, 'Road Bike', '<Root>  <ProductDescription ProductID="1" ProductName="Road Bike">  <Features>  <Warranty>1 year parts and labor</Warranty>  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>  </Features>  </ProductDescription>  </Root>'),
        (2, 'Mountain Bike', '<Root>  <ProductDescription ProductID="2" ProductName="Mountain Bike">  <Features>  <Warranty>2 year parts and labor</Warranty>  <Maintenance>4 year parts and labor extended maintenance is available</Maintenance>  </Features>  </ProductDescription>  </Root>')
) AS T (ProductID, ProductName, ProductDescription);