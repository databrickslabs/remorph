--Query type: DML
DECLARE @ProductModel TABLE (ProductModelID INT, Instructions XML);
INSERT INTO @ProductModel (ProductModelID, Instructions)
VALUES (1, '<root xmlns:MI="https://schemas.microsoft.com/sqlserver/2004/07/adventure-works/ProductModelManuInstructions"><MI:Location LocationID="1000"><MI:step>Step 1</MI:step><MI:step>Step 2</MI:step></MI:Location></root>');
UPDATE @ProductModel
SET Instructions.modify('declare namespace MI="https://schemas.microsoft.com/sqlserver/2004/07/adventure-works/ProductModelManuInstructions"; delete(/MI:root/MI:Location[@LocationID=1000]/MI:step[2])');
SELECT * FROM @ProductModel;
-- REMORPH CLEANUP: DROP TABLE @ProductModel;
