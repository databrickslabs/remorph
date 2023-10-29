-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/output-clause-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

IF OBJECT_ID('dbo.vw_ScrapReason', 'V') IS NOT NULL
    DROP VIEW dbo.vw_ScrapReason;
GO

CREATE VIEW dbo.vw_ScrapReason
AS
SELECT ScrapReasonID,
    Name,
    ModifiedDate
FROM Production.ScrapReason;
GO

CREATE TRIGGER dbo.io_ScrapReason ON dbo.vw_ScrapReason
INSTEAD OF INSERT
AS
BEGIN
    --ScrapReasonID is not specified in the list of columns to be inserted
    --because it is an IDENTITY column.
    INSERT INTO Production.ScrapReason (
        Name,
        ModifiedDate
    )
    OUTPUT INSERTED.ScrapReasonID,
        INSERTED.Name,
        INSERTED.ModifiedDate
    SELECT Name, GETDATE()
    FROM INSERTED;
END
GO

INSERT vw_ScrapReason (
    ScrapReasonID,
    Name,
    ModifiedDate
)
VALUES (
    99,
    N'My scrap reason',
    '20030404'
);
GO