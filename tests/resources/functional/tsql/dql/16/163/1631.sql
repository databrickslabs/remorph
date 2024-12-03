--Query type: DQL
WITH geography_data AS ( SELECT geography::STGeomFromText('LINESTRING(-122.360 47.656, -122.343 47.656)', 4326) AS geom1, geography::STGeomFromText('POINT(-122.34900 47.65100)', 4326) AS geom2 ) SELECT geom1.STDistance(geom2) AS distance FROM geography_data
