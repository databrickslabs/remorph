-- tsql sql:
DECLARE @myXml XML;
SET @myXml = (
    SELECT *
    FROM (
        VALUES ('<Root> <ProductDescription ProductID="1" ProductName="Road Bike"> <Features> </Features> </ProductDescription> </Root>')
    ) AS T(XmlColumn)
);
SELECT @myXml;
SET @myXml.modify(' insert <Maintenance>3 year parts and labor extended maintenance is available</Maintenance> into (/Root/ProductDescription/Features)[1]');
SELECT @myXml;
SET @myXml.modify(' insert <Warranty>1 year parts and labor</Warranty> as first into (/Root/ProductDescription/Features)[1]');
SELECT @myXml;
SET @myXml.modify(' insert <Material>Aluminium</Material> as last into (/Root/ProductDescription/Features)[1]');
SELECT @myXml;
SET @myXml.modify(' insert <BikeFrame>Strong long lasting</BikeFrame> after (/Root/ProductDescription/Features/Material)[1]');
SELECT @myXml;
