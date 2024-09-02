--Query type: DQL
DECLARE @customer geography;
SET @customer = geography::STGeomFromText('POINT(-122.34900 47.65100)', 4326);
SELECT @customer.Long AS customer_longitude, @customer.Lat AS customer_latitude, @customer.STSrid AS customer_srid;