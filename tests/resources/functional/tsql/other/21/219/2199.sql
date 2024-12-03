--Query type: DML
WITH MeasureCTE AS (
    SELECT N'Cubic Meters' AS Name, N'M3' AS MeasureCode, GETDATE() AS ModifiedDate
    UNION ALL
    SELECT N'Square Feet', N'FT2', GETDATE()
    UNION ALL
    SELECT N'Liters', N'L', GETDATE()
)
INSERT INTO Sales.Measure (Name, MeasureCode, ModifiedDate)
SELECT Name, MeasureCode, ModifiedDate
FROM MeasureCTE;
