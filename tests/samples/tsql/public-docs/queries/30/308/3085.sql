-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/output-clause-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

DECLARE @MyTableVar TABLE (
    SummaryBefore NVARCHAR(max),
    SummaryAfter NVARCHAR(max));
  
UPDATE Production.Document
SET DocumentSummary .WRITE (N'features',28,10)
OUTPUT DELETED.DocumentSummary,
       INSERTED.DocumentSummary
    INTO @MyTableVar
WHERE Title = N'Front Reflector Bracket Installation';
  
SELECT SummaryBefore, SummaryAfter
FROM @MyTableVar;
GO