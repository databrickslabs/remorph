--Query type: DQL
SELECT RegionID, RegionName FROM (VALUES (1, 'North'), (2, 'South'), (3, 'East'), (4, 'West')) AS Region(RegionID, RegionName) WHERE RegionID > 2 ORDER BY RegionID;
