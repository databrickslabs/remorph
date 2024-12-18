-- tsql sql:
WITH GeoCTE AS ( SELECT geography::STGeomFromText('LINESTRING(-122.360 47.656, -122.343 47.656)', 4326) AS Geo ) SELECT Geo.STPointN(2).ToString() FROM GeoCTE;
