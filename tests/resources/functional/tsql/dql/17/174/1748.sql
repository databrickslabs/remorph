--Query type: DQL
WITH geom_data AS ( SELECT geometry::STGeomFromText('MULTIPOINT(1 1, 14.5 3, 8 20)', 0) AS geom ) SELECT geom.InstanceOf('GEOMETRYCOLLECTION') AS is_geom_collection FROM geom_data;