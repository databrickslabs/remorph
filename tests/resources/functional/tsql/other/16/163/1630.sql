-- tsql sql:
DECLARE @g geography;
WITH location AS (
    SELECT geography::Point(47.65100, -122.34900, 4326) AS location
)
SELECT location.ToString()
FROM location;
