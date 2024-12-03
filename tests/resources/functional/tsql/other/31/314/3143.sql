--Query type: DML
IF OBJECT_ID('dbo.KneePads', 'U') IS NOT NULL
    DROP TABLE dbo.KneePads;

SELECT ProductModelID, Name
INTO dbo.KneePads
FROM (
    VALUES (5, 'Soft Knee Pads'),
           (6, 'Hard Knee Pads')
) AS ProductModel (ProductModelID, Name)
WHERE ProductModelID IN (5, 6);
