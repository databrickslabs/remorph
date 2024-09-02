--Query type: DQL
SELECT geography::ConvexHullAggregate(Region).ToString() AS RegionBoundary
FROM (
    VALUES ('1', geography::Point(47.65100, -122.34900, 4326)),
         ('2', geography::Point(47.65100, -122.34900, 4326))
) AS RegionTable (RegionID, Region)
WHERE RegionID LIKE ('1');