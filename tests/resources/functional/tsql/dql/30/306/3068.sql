--Query type: DQL
SELECT geography::CollectionAggregate(Region).ToString() AS RegionLocation
FROM (
    VALUES ('Seattle', geography::Point(47.6067, -122.3321, 4326)),
           ('New York', geography::Point(40.7128, -74.0060, 4326))
) AS RegionTable (City, Region)
WHERE City LIKE 'Seattle';