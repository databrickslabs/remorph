--Query type: DML
WITH CurveData AS (
    SELECT geography::STGeomFromText('CURVEPOLYGON (CIRCULARSTRING (0 0, 1 1, 1 0, 0 0))', 4326) AS Curve
),
LineData AS (
    SELECT Curve.STCurveToLine() AS Line
    FROM CurveData
)
SELECT Line.ToString() AS LineString
FROM LineData;
-- REMORPH CLEANUP: DROP TABLE CurveData;
-- REMORPH CLEANUP: DROP TABLE LineData;
