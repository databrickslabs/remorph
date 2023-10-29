-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-index-transact-sql?view=sql-server-ver16

-- Verify the existing value.
SELECT Name FROM Production.UnitMeasure WHERE Name = N'Ounces';
GO

INSERT INTO Production.UnitMeasure (UnitMeasureCode, Name, ModifiedDate)
  VALUES ('OC', 'Ounces', GETDATE());