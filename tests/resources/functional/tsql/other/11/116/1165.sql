--Query type: DDL
CREATE TABLE #temp_table ( geometry_col geometry );
INSERT INTO #temp_table ( geometry_col )
VALUES ( geometry::STGeomFromText( 'POINT(1 1)', 0 ) );
CREATE SPATIAL INDEX SIndx_SpatialTable_geometry_col3
ON #temp_table ( geometry_col )
WITH ( BOUNDING_BOX = ( 0, 0, 500, 200 ), GRIDS = ( LEVEL_4 = HIGH, LEVEL_3 = MEDIUM ) );
SELECT *
FROM #temp_table;
-- REMORPH CLEANUP: DROP TABLE #temp_table;
