-- tsql sql:
DECLARE @customer_location geography;
SET @customer_location = geography::STGeomFromText('POINT(-74.00600 40.71280)', 4326);
SELECT Long FROM (VALUES (@customer_location.Long)) AS temp_result(Long);
