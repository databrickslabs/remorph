--Query type: DQL
DECLARE @g geography = 'POLYGON ((-71.0882 42.315, -71.0882 42.32, -71.0782 42.32, -71.0782 42.315, -71.0882 42.315))';
DECLARE @h geography = 'POLYGON ((-71.0782 42.315, -71.0782 42.32, -71.0682 42.32, -71.0682 42.315, -71.0782 42.315))';
SELECT @g.STUnion(@h).ToString();
