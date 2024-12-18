-- tsql sql:
DECLARE @customer geography = 'POLYGON((-122.358 47.653, -122.348 47.649, -122.348 47.658, -122.358 47.658, -122.358 47.653))';
WITH customer_location AS (
    SELECT @customer AS location
)
SELECT location.STSymDifference('FULLGLOBE').ToString() AS sym_diff
FROM customer_location;
