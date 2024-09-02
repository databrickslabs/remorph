--Query type: DML
DECLARE @x XML;
DECLARE @f INT;

SELECT @x = Instructions
FROM (
    VALUES ('<root xmlns="https://schemas.microsoft.com/sqlserver/2004/07/adventure-works/ProductModelManuInstructions"><Location LocationID="50">Location 1</Location></root>')
) AS ProductModelCTE(Instructions)
WHERE Instructions IS NOT NULL;

SET @f = @x.exist('/root/Location[@LocationID=50]');

SELECT @f AS Result;