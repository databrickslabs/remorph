--Query type: DML
WITH TempResult AS ( SELECT 'GEOMETRYCOLLECTION ( POINT(-122.34900 47.65100), LINESTRING(-122.360 47.656, -122.343 47.656) )' AS geom_text ) SELECT geography::STGeomCollFromText(geom_text, 4326) AS geom FROM TempResult;
