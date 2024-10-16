--Query type: DML
DECLARE @ProductModel TABLE (ProductModelID INT, Instructions XML);
INSERT INTO @ProductModel (ProductModelID, Instructions)
VALUES (1, '<root xmlns:MI="https://schemas.microsoft.com/sqlserver/2004/07/adventure-works/ProductModelManuInstructions"><MI:Location LocationID="1000" LaborHours="10"/></root>');
UPDATE @ProductModel
SET Instructions.modify('declare namespace MI="https://schemas.microsoft.com/sqlserver/2004/07/adventure-works/ProductModelManuInstructions"; delete(/MI:root/MI:Location[@LocationID=1000]/@LaborHours)');
SELECT * FROM @ProductModel;