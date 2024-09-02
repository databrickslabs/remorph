--Query type: DQL
DECLARE @g geometry;
SET @g = geometry::STGeomFromText('POLYGON((-122.358 47.653, -122.348 47.649, -122.348 47.658, -122.358 47.658, -122.358 47.653))', 4326);
SELECT @g.STGeometryType() AS geom_type
FROM (VALUES (1)) AS temp_table(temp_column);