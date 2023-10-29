-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/output-clause-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

DECLARE @MyTestVar TABLE (
    OldScrapReasonID INT NOT NULL,
    NewScrapReasonID INT NOT NULL,
    WorkOrderID INT NOT NULL,
    ProductID INT NOT NULL,
    ProductName NVARCHAR(50)NOT NULL);
  
UPDATE Production.WorkOrder
SET ScrapReasonID = 4
OUTPUT DELETED.ScrapReasonID,
       INSERTED.ScrapReasonID,
       INSERTED.WorkOrderID,
       INSERTED.ProductID,
       p.Name
    INTO @MyTestVar
FROM Production.WorkOrder AS wo
    INNER JOIN Production.Product AS p
    ON wo.ProductID = p.ProductID
    AND wo.ScrapReasonID= 16
    AND p.ProductID = 733;
  
SELECT OldScrapReasonID, NewScrapReasonID, WorkOrderID,
    ProductID, ProductName
FROM @MyTestVar;
GO