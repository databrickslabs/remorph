--Query type: DDL
CREATE TABLE #tmp ( geo geography );
INSERT INTO #tmp ( geo )
VALUES ( geography::Point( 1, 1, 4326 ) );
CREATE SPATIAL INDEX idx_region_geo
ON #tmp ( geo )
WITH (
    BOUNDING_BOX = ( -180, -90, 180, 90 ),
    GRIDS = ( LEVEL_1 = MEDIUM, LEVEL_2 = HIGH, LEVEL_3 = MEDIUM ),
    CELLS_PER_OBJECT = 16,
    DROP_EXISTING = ON
);
SELECT *
FROM #tmp;
-- REMORPH CLEANUP: DROP TABLE #tmp;