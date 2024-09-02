--Query type: DQL
DECLARE @customer_location geography;
SET @customer_location = geography::Parse('COMPOUNDCURVE(CIRCULARSTRING(-122.358 47.653, -122.348 47.649, -122.348 47.658, -122.358 47.658, -122.358 47.653))');
SELECT location.STNumCurves()
FROM (
    VALUES (@customer_location)
) AS temp_result(location);