--Query type: DDL
CREATE TABLE dbo.Regions
WITH (DISTRIBUTION = ROUND_ROBIN)
AS
SELECT RegionName, RegionState, RegionLocation
FROM (
    VALUES ('North', 'WA', GEOGRAPHY::Point(47.65100, -122.34900, 4326)),
         ('South', 'TX', GEOGRAPHY::Point(29.76040, -95.36980, 4326))
) AS tmp (RegionName, RegionState, RegionLocation);