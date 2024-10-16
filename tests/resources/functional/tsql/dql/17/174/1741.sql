--Query type: DQL
WITH temp_result AS ( SELECT geometry::STGeomFromText('LINESTRING(1 1, 3 3, 2 1)', 0) AS geom ) SELECT geom.STNumPoints() AS num_points FROM temp_result;