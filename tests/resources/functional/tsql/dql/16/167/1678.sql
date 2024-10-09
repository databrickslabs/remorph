--Query type: DQL
WITH geography_data AS ( SELECT geography::Parse('LINESTRING(-122.360 47.656, -122.343 47.656)') AS geo ) SELECT geo.ToString() FROM geography_data