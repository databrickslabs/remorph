-- tsql sql:
CREATE TABLE #UnitMeasure
(
    UnitMeasureCode nvarchar(3),
    Name nvarchar(25),
    ModifiedDate datetime
);

INSERT INTO #UnitMeasure
SELECT UnitMeasureCode, Name, ModifiedDate
FROM (
    VALUES (N'FT2', N'Square Feet ', '20080923'),
           (N'Y', N'Yards', '20080923'),
           (N'Y3', N'Cubic Yards', '20080923')
) AS MyUnitMeasure(UnitMeasureCode, Name, ModifiedDate);

SELECT *
FROM #UnitMeasure;
-- REMORPH CLEANUP: DROP TABLE #UnitMeasure;
