-- see https://docs.snowflake.com/en/sql-reference/functions/st_asgeojson

SELECT ST_ASGEOJSON(TO_GEOMETRY('SRID=4326;LINESTRING(389866 5819003, 390000 5830000)')) AS geojson;