-- tsql sql:
DECLARE @h geography;
SET @h = geography::Parse('POLYGON((-122.3 47.45, -118.283 46.1, -120.533 46.566, -122.3 47.45))');
WITH temp AS (
    SELECT @h.STConvexHull().ToString() AS result
)
SELECT * FROM temp;
