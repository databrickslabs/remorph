-- tsql sql:
DECLARE @customer geography;
SET @customer = geography::STGeomFromText('POINT(-122.360 47.656)', 4326);
WITH customer_location AS (
    SELECT @customer.STStartPoint().ToString() AS start_point
)
SELECT start_point
FROM customer_location;
